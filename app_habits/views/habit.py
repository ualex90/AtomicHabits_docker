from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticated

from app_habits.models import Habit
from app_habits.paginators.habit import HabitPaginator
from app_habits.serializers.habit import (
    HabitGoodCreateSerializer,
    HabitNiceCreateSerializer,
    HabitListSerializer,
    HabitListAllSerializer,
    HabitSerializer, HabitGoodUpdateSerializer,
)
from app_habits.services import add_task, update_task, delete_task
from app_users.permissions import IsModerator, IsOwner, IsPublic


class HabitNiceCreateAPIView(CreateAPIView):
    """
    Создание приятной привычки

    Создавать может любой авторизованный пользователь не являющийся модератором
    """

    queryset = Habit.objects.all()
    serializer_class = HabitNiceCreateSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_habit = serializer.save()

        new_habit.owner = self.request.user  # Добавляем пользователя
        new_habit.is_nice = True  # Устанавливаем признак приятной привычки

        new_habit.save()


class HabitGoodCreateAPIView(CreateAPIView):
    """
    Создание полезной привычки

    Создавать может любой авторизованный пользователь не являющийся модератором
    """
    queryset = Habit.objects.all()
    serializer_class = HabitGoodCreateSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_habit = serializer.save()

        new_habit.owner = self.request.user  # Добавляем пользователя

        new_habit.save()

        add_task(new_habit)  # Создаем периодическую задачу


class HabitListAPIView(ListAPIView):
    """
    Получение списка привычек

    - Доступна фильтрация по признаку приятной привычки
      is_nice (true, false)
    - Сортировка по любому доступному полю
      (для админа, дополнительно owner_email)

    Просматривать пользователь может только свои привычки
    Модератор просматривает все привычки с указанием создателя
    """

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = None
    filterset_fields = ('is_nice', )
    pagination_class = HabitPaginator

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Habit.objects.all()
        else:
            queryset = Habit.objects.filter(owner=self.request.user)

        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_staff:
            serializer_class = HabitListAllSerializer
            self.ordering_fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice', 'owner_email', )
        else:
            serializer_class = HabitListSerializer
            self.ordering_fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice', )

        return serializer_class


class HabitRetrieveAPIView(RetrieveAPIView):
    """
    Подробный просмотр привычки

    Просматривать разрешено создателю, модератору либо любому пользователю если привычка публичная
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsPublic | IsOwner | IsModerator]


class HabitPublicListAPIView(ListAPIView):
    """
    Получение списка публичных привычек

    - Доступна фильтрация по признаку приятной привычки
      is_nice (true, false)
    - Сортировка по любому доступному полю.

    Просматривать может любой авторизованный пользователь
    """

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitListAllSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ('id', 'task', 'start_time', 'location', 'periodicity', 'is_nice', 'owner_email', )
    filterset_fields = ('is_nice', )
    pagination_class = HabitPaginator


class HabitUpdateAPIView(UpdateAPIView):
    """
    Изменение привычки

    Изменять разрешено владельцу либо модератору
    """

    queryset = Habit.objects.all()
    permission_classes = [IsOwner | IsModerator]

    def get_serializer_class(self):
        if self.get_object().is_nice:
            return HabitNiceCreateSerializer
        return HabitGoodUpdateSerializer

    def perform_update(self, serializer):
        obj = serializer.save()
        # Изменяем периодическую задачу если она существует
        update_task(obj)


class HabitDestroyAPIView(DestroyAPIView):
    """
    Удаление привычки

    Удалять может только создатель
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]

    def perform_destroy(self, instance):
        # Удаляем периодическую задачу если она существует
        delete_task(instance)
        # Удаляем привычку
        instance.delete()
