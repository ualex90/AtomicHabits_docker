from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from app_users.models import User
from app_users.serializers.user import RegisterUserSerializer, RegisterUserResponseSerializer


class RegisterUserAPIView(CreateAPIView):
    """
    Регистрация нового пользователя

    Создание нового пользователя с проверкой валидности данных
    Минимальный набор данных:
    - email: электронная почта
    - password: пароль
    - password_again: пароль повторно
    """

    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    # Оборачиваем в декоратор для отображения в документации.
    # НА ЛОГИКУ РАБОТЫ НЕ ВЛИЯЕТ!!!
    @swagger_auto_schema(responses={
        201: RegisterUserResponseSerializer(many=True),  # Переопределение сериализатора для ответа по статусу 201
    })
    def post(self, request, *args, **kwargs):
        # Добавляем RegisterUserSerializer
        serializer = RegisterUserSerializer(data=request.data)
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            serializer.save()
            # Возвращаем что всё в порядке
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
