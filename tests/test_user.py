from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app_users.models import User


class UserTest(APITestCase):

    def setUp(self):
        pass

    def test_register(self):
        """ Тестирование регистрации нового пользователя """

        # Проверяем количество пользователей в базе данных
        users_count1 = User.objects.all().count()

        data = {
            "email": "user_register_test@sky.pro",
            "password": "123qwe",
            "password_again": "123qwe",
            "first_name": "Test_first_name",
            "last_name": "Test_last_name",
            "telegram_id": "123456789",
        }

        response = self.client.post(
            reverse("app_users:register"),
            data=data
        )

        # Проверяем количество пользователей в базе данных
        users_count2 = User.objects.all().count()

        # Проверяем что пользователь успешно создан
        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверяем ответ
        self.assertEquals(
            response.json(),
            {
                'email': 'user_register_test@sky.pro',
                'first_name': 'Test_first_name',
                'last_name': 'Test_last_name',
                'telegram_id': "123456789"
            }
        )

        # Проверяем что пользователь появился в базе данных
        self.assertTrue(
            users_count1 == (users_count2 - 1)
        )

    def test_invalid_password_register(self):
        """
        Тестирование проверки совпадения паролей
        и невозможности создания пользователя в случае ошибки
        """

        # Проверяем количество пользователей в базе данных
        users_count1 = User.objects.all().count()

        data = {
            "email": "user_register_test@sky.pro",
            "password": "123qwe",
            "password_again": "qwe123",
            "telegram_id": "123456789",
        }

        response = self.client.post(
            reverse("app_users:register"),
            data=data
        )

        # Проверяем количество пользователей в базе данных
        users_count2 = User.objects.all().count()

        # Проверяем что вернулась ошибка
        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        # Проверяем ответ
        self.assertEquals(
            response.json(),
            {
                'detail': 'Введенные пароли не совпадают'
            }
        )

        # Проверяем что пользователь появился в базе данных
        self.assertTrue(
            users_count1 == users_count2
        )
