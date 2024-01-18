from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app_habits.models import Habit
from app_users.models import User


class HabitTest(APITestCase):

    def setUp(self):
        # User_1
        self.user_1 = User.objects.create(
            email="user1@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_1.set_password('test')
        self.user_1.save()

        self.nice_habit_1 = Habit.objects.create(
            task="Test nice habit 1",
            location="Test location 1",
            is_nice=True,
            owner=self.user_1
        )

        self.good_habit_1 = Habit.objects.create(
            task="Test good habit 1",
            location="Test location 1",
            is_nice=False,
            related_habit=self.nice_habit_1,
            owner=self.user_1
        )

        self.good_habit_2 = Habit.objects.create(
            task="Test good habit 2",
            location="Test location 2",
            is_nice=False,
            reward="Test reward 1",
            is_public=True,
            owner=self.user_1
        )

        # User_2
        self.user_2 = User.objects.create(
            email="user2@test.com",
            is_staff=False,
            is_active=True,
        )
        self.user_2.set_password('test')
        self.user_2.save()

        self.nice_habit_2 = Habit.objects.create(
            task="Test nice habit 2",
            location="Test location 2",
            is_nice=True,
            is_public=True,
            owner=self.user_2
        )

        self.good_habit_3 = Habit.objects.create(
            task="Test good habit 3",
            location="Test location 3",
            is_nice=False,
            related_habit=self.nice_habit_2,
            owner=self.user_2
        )

        self.good_habit_4 = Habit.objects.create(
            task="Test good habit 4",
            location="Test location 4",
            is_nice=False,
            reward="Test reward 2",
            owner=self.user_2
        )

        # Moderator
        self.moderator = User.objects.create(
            email="moderator@test.com",
            is_staff=True,
            is_active=True,
        )
        self.moderator.set_password('test')
        self.moderator.save()

    def test_list_for_user(self):
        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(
            reverse("app_habits:habit_list")
        )

        self.assertEquals(
            response.json(),
            {
                'count': 3,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.nice_habit_1.id,
                        'task': 'Test nice habit 1',
                        'start_time': None,
                        'location': 'Test location 1',
                        'periodicity': '1',
                        'is_nice': True
                    },
                    {
                        'id': self.good_habit_1.id,
                        'task': 'Test good habit 1',
                        'start_time': None,
                        'location': 'Test location 1',
                        'periodicity': '1',
                        'is_nice': False
                    },
                    {
                        'id': self.good_habit_2.id,
                        'task': 'Test good habit 2',
                        'start_time': None,
                        'location': 'Test location 2',
                        'periodicity': '1',
                        'is_nice': False
                    }
                ]
            }
        )

    def test_list_for_moderator(self):
        # Аутентифицируем модератора
        self.client.force_authenticate(user=self.moderator)

        response = self.client.get(
            reverse("app_habits:habit_list")
        )

        self.assertEquals(
            response.json(),
            {
                'count': 6,
                'next': 'http://testserver/habit/list/?page=2',
                'previous': None,
                'results': [
                    {
                        'id': self.nice_habit_1.id,
                        'task': 'Test nice habit 1',
                        'start_time': None,
                        'location': 'Test location 1',
                        'periodicity': '1',
                        'is_nice': True,
                        'owner_email': 'user1@test.com'
                    },
                    {
                        'id': self.good_habit_1.id,
                        'task': 'Test good habit 1',
                        'start_time': None,
                        'location': 'Test location 1',
                        'periodicity': '1',
                        'is_nice': False,
                        'owner_email': 'user1@test.com'
                    },
                    {
                        'id': self.good_habit_2.id,
                        'task': 'Test good habit 2',
                        'start_time': None,
                        'location': 'Test location 2',
                        'periodicity': '1',
                        'is_nice': False,
                        'owner_email': 'user1@test.com'
                    },
                    {
                        'id': self.nice_habit_2.id,
                        'task': 'Test nice habit 2',
                        'start_time': None,
                        'location': 'Test location 2',
                        'periodicity': '1',
                        'is_nice': True,
                        'owner_email': 'user2@test.com'
                    },
                    {
                        'id': self.good_habit_3.id,
                        'task': 'Test good habit 3',
                        'start_time': None,
                        'location': 'Test location 3',
                        'periodicity': '1',
                        'is_nice': False,
                        'owner_email': 'user2@test.com'
                    }
                ]
            }
        )

    def test_permission_anonim_list(self):
        """
        Тестирование ограничение при просмотре
        привычки без аутентификации
        """

        response = self.client.get(
            reverse("app_habits:habit_list")
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_public_list(self):
        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(
            reverse("app_habits:habit_public_list")
        )

        self.assertEquals(
            response.json(),
            {
                'count': 2,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.good_habit_2.id,
                        'task': 'Test good habit 2',
                        'start_time': None,
                        'location': 'Test location 2',
                        'periodicity': '1',
                        'is_nice': False,
                        'owner_email': 'user1@test.com'
                    },
                    {
                        'id': self.nice_habit_2.id,
                        'task': 'Test nice habit 2',
                        'start_time': None,
                        'location': 'Test location 2',
                        'periodicity': '1',
                        'is_nice': True,
                        'owner_email': 'user2@test.com'
                    }
                ]
            }
        )

    def test_permission_anonim_public_list(self):
        """
        Тестирование ограничение при просмотре
        привычки без аутентификации
        """

        response = self.client.get(
            reverse("app_habits:habit_public_list")
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_retrieve(self):
        """
        Подробный просмотр привычки создателем привычки
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Создаем привычку
        habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            owner=self.user_1
        )

        response = self.client.get(
            reverse("app_habits:habit_retrieve", kwargs={'pk': habit.id})
        )

        self.assertEquals(
            response.json(),
            {
                'id': habit.id,
                'task': 'Test good habit',
                'start_time': None,
                'location': 'Test location',
                'is_nice': False,
                'periodicity': '1',
                'reward': None,
                'time_to_complete': 60,
                'is_public': False,
                'owner': self.user_1.id,
                'related_habit': None
            }
        )

    def test_moderator_retrieve(self):
        """
        Подробный просмотр привычки модератором
        """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.moderator)

        # Создаем привычку
        habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            owner=self.user_1
        )

        response = self.client.get(
            reverse("app_habits:habit_retrieve", kwargs={'pk': habit.id})
        )

        self.assertEquals(
            response.json(),
            {
                'id': habit.id,
                'task': 'Test good habit',
                'start_time': None,
                'location': 'Test location',
                'is_nice': False,
                'periodicity': '1',
                'reward': None,
                'time_to_complete': 60,
                'is_public': False,
                'owner': self.user_1.id,
                'related_habit': None
            }
        )

    def test_public_retrieve(self):
        """
        Подробный просмотр публичной привычки
        """

        # Создаем привычку
        habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            is_public=True,
            owner=self.user_1,
        )

        # Аутентифицируем другого пользователя
        self.client.force_authenticate(user=self.user_2)

        response = self.client.get(
            reverse("app_habits:habit_retrieve", kwargs={'pk': habit.id})
        )

        self.assertEquals(
            response.json(),
            {
                'id': habit.id,
                'task': 'Test good habit',
                'start_time': None,
                'location': 'Test location',
                'is_nice': False,
                'periodicity': '1',
                'reward': None,
                'time_to_complete': 60,
                'is_public': True,
                'owner': self.user_1.id,
                'related_habit': None
            }
        )

    def test_permission_anonim_retrieve(self):
        """
        Тестирование ограничений прав
        доступа при просмотре непубличной
        привычки без авторизации
        """

        response = self.client.delete(
            reverse("app_habits:habit_destroy", kwargs={'pk': self.good_habit_1.id})
        )

        # Проверяем ошибку доступа
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_permission_other_user_retrieve(self):
        """
        Тестирование ограничений прав
        доступа при просмотре непубличной
        привычки другим пользователем
        """

        # Аутентифицируем обычного пользователя отличного от создателя привычки
        self.client.force_authenticate(user=self.user_2)

        response = self.client.delete(
            reverse("app_habits:habit_destroy", kwargs={'pk': self.good_habit_1.id})
        )

        # Проверяем ошибку доступа
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_destroy(self):
        """ Тестирование удаления """

        # Аутентифицируем обычного пользователя
        self.client.force_authenticate(user=self.user_1)

        # Создаем привычку
        habit = Habit.objects.create(
            task="Test good habit",
            location="Test location",
            is_nice=False,
            owner=self.user_1
        )

        # считаем количество привычек в базе данных до удаления
        count_habit_1 = Habit.objects.all().count()

        # Изменяем привычку
        self.client.delete(
            reverse("app_habits:habit_destroy", kwargs={'pk': habit.id})
        )

        # считаем количество привычек в базе данных после удаления
        count_habit_2 = Habit.objects.all().count()

        self.assertTrue(
            count_habit_1 - 1 == count_habit_2
        )

    def test_permission_other_user_destroy(self):
        """
        Тестирование ограничений прав
        доступа при удалении привычки
        другим пользователем
        """

        # Аутентифицируем обычного пользователя отличного от создателя привычки
        self.client.force_authenticate(user=self.user_2)

        response = self.client.delete(
            reverse("app_habits:habit_destroy", kwargs={'pk': self.good_habit_1.id})
        )

        # Проверяем ошибку доступа
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_permission_moderator_destroy(self):
        """
        Тестирование ограничений прав
        доступа при удалении привычки
        модератором
        """

        # Аутентифицируем модератора
        self.client.force_authenticate(user=self.moderator)

        response = self.client.delete(
            reverse("app_habits:habit_destroy", kwargs={'pk': self.good_habit_1.id})
        )

        # Проверяем ошибку доступа
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_permission_anonim_destroy(self):
        """
        Тестирование ограничение при удалении
        привычки без аутентификации
        """

        response = self.client.delete(
            reverse("app_habits:habit_destroy", kwargs={'pk': self.good_habit_1.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
