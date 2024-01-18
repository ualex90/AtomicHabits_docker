from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app_habits.models import Habit
from app_users.models import User


class HabitNiceTest(APITestCase):

    def setUp(self):
        # Users
        self.user_1 = User.objects.create(
            email="user1@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_1.set_password('test')
        self.user_1.save()

        self.user_2 = User.objects.create(
            email="user2@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_2.set_password('test')
        self.user_2.save()

        self.user_3 = User.objects.create(
            email="user3@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_3.set_password('test')
        self.user_3.save()

    def test_create(self):
        """ Тестирование создания объекта с минимальным набором полей """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task nice",
            "location": "Test location",
        }

        response = self.client.post(
            reverse("app_habits:habit_nice_create"),
            data=data
        )

        # Проверяем что объект успешно создан
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем ответ
        self.assertEquals(
            response.json(),
            {
                "id": response.json().get("id"),
                "task": "Test task nice",
                "location": "Test location",
                "is_nice": True,
                "time_to_complete": 60,
                "is_public": False,
                "owner": self.user_1.id
            }
        )

    def test_time_to_complete_validator(self):
        """
        Тестирование валидатора TimeToCompleteValidator
        при превышении значения времени выполнения (ограничено 120)
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task good",
            "location": "Test location",
            "time_to_complete": 121
        }

        response = self.client.post(
            reverse("app_habits:habit_nice_create"),
            data=data
        )

        # Проверяем что получили ошибку
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверяем текст ответа
        self.assertEquals(
            response.json(),
            {'non_field_errors': ['Время выполнения задания не должно превышать 120 секунд']}
        )

    def test_not_related(self):
        """
        Тестирование на уровне модели
        Невозможность задания связанной привычки для полезной привычки
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task good",
            "location": "Test location",
            "related_habit": 1
        }

        response = self.client.post(
            reverse("app_habits:habit_nice_create"),
            data=data
        )

        # Проверяем что объект успешно создан
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем что в поле related_habit отсутствуют данные
        self.assertTrue(
            not Habit.objects.get(pk=response.json().get("id")).related_habit
        )

    def test_not_reward(self):
        """
        Тестирование на уровне модели
        Невозможность задания вознаграждения для полезной привычки
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        data = {
            "task": "Test task good",
            "location": "Test location",
            "reward": "Test reward"
        }

        response = self.client.post(
            reverse("app_habits:habit_nice_create"),
            data=data
        )

        # Проверяем что объект успешно создан
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем что в поле reward отсутствуют данные
        self.assertTrue(
            not Habit.objects.get(pk=response.json().get("id")).reward
        )

    def test_permission_anonim_created(self):
        """
        Тестирование ограничение при создании
        привычки без аутентификации
        """

        data = {
            "task": "Test task good",
            "location": "Test location",
            "reward": "Test reward"
        }

        response = self.client.post(
            reverse("app_habits:habit_nice_create"),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_update(self):
        """ Тестирование изменения """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Создаем приятную привычку
        nice_habit = Habit.objects.create(
            task="Test nice habit",
            location="Test location",
            is_nice=True,
            owner=self.user_1
        )

        # Изменяем привычку
        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': nice_habit.id}),
            data={
                'time_to_complete': 111,
                'is_public': True,
            }
        )

        self.assertEquals(
            response.json(),
            {
                'id': nice_habit.id,
                'task': 'Test nice habit',
                'location': 'Test location',
                'is_nice': True,
                'time_to_complete': 111,
                'is_public': True,
                'owner': self.user_1.id,
            }
        )

    def test_permission_anonim_update(self):
        """
        Тестирование ограничение при изменении
        привычки без аутентификации
        """

        nice_habit = Habit.objects.create(
            task="Test nice habit",
            location="Test location",
            is_nice=True,
            owner=self.user_1
        )

        # Изменяем привычку
        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': nice_habit.id}),
            data={
                'time_to_complete': 111,
                'is_public': True,
            }
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_permission_other_user_update(self):
        """
        Тестирование ограничение при изменении
        привычки без аутентификации
        """

        # Создаем полезную привычку
        nice_habit = Habit.objects.create(
            task="Test nice habit",
            location="Test location",
            is_nice=True,
            owner=self.user_1
        )

        # Аутентифицируем другого пользователя
        self.client.force_authenticate(user=self.user_2)

        # Изменяем привычку
        response = self.client.patch(
            reverse("app_habits:habit_update", kwargs={'pk': nice_habit.id}),
            data={
                'time_to_complete': 111,
                'is_public': True,
            }
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
