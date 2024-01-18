from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from app_users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации нового пользователя

    Выполняется проверка повторного введения пароля
    """

    password_again = serializers.CharField(
        max_length=128,
        label=_("Password (again)"),
        write_only=True
    )

    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = User(
            # Назначаем Email и при наличии first_name, last_name
            email=self.validated_data['email'],
            first_name=self.validated_data.get('first_name') if self.validated_data.get('first_name') else "",
            last_name=self.validated_data.get('last_name') if self.validated_data.get('last_name') else "",
            telegram_id=self.validated_data.get('telegram_id') if self.validated_data.get('telegram_id') else "",
        )
        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password_again = self.validated_data['password_again']
        # Проверяем совпадают ли пароли
        if password != password_again:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({'detail': "Введенные пароли не совпадают"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя
        return user

    class Meta:
        model = User
        fields = ('email', 'password', 'password_again', 'first_name', 'last_name', 'telegram_id')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class RegisterUserResponseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для формирования ответа RegisterUserSerializer
    для формирования документации DRF YASG
    """

    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    telegram_id = serializers.CharField(max_length=10)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'telegram_id', )
