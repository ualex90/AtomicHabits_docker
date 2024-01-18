from django.db import models

from app_users.models import NULLABLE
from config import settings


class Periodicity(models.TextChoices):
    """ Период выполнения привычки """

    DAY_1 = 1, '1 День'
    DAY_2 = 2, '2 Дня'
    DAY_3 = 3, '3 Дня'
    DAY_4 = 4, '4 Дня'
    DAY_5 = 5, '5 Дней'
    DAY_6 = 6, '6 Дней'
    DAY_7 = 7, '7 Дней'


class Habit(models.Model):
    """
    Модель "привычка".
    Модель универсальная.
    На ее основе создается как полезная, так и приятная привычка
    """
    #
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Создатель привычки',
        **NULLABLE
    )
    #
    task = models.TextField(
        verbose_name='Выполняемое действие'
    )
    # ДЛЯ ПОЛЕЗНОЙ привычки
    start_time = models.TimeField(
        verbose_name='Время начала выполнения',
        **NULLABLE
    )
    #
    location = models.CharField(
        max_length=50,
        verbose_name='Место выполнения действия'
    )
    #
    is_nice = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    # ДЛЯ ПОЛЕЗНОЙ привычки
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name='Привязка приятной привычки',
        **NULLABLE
    )
    # ДЛЯ ПОЛЕЗНОЙ привычки. Минимум - 1 день, максимум - 7 дней с шагом в 1 день
    periodicity = models.CharField(
        default=Periodicity.DAY_1,
        max_length=2,
        choices=Periodicity.choices,
        verbose_name='Периодичность дней',
        **NULLABLE
    )
    # ДЛЯ ПОЛЕЗНОЙ привычки
    reward = models.CharField(
        max_length=50,
        verbose_name="Вознаграждение",
        **NULLABLE
    )
    # Не более 120 секунд
    time_to_complete = models.PositiveIntegerField(
        default=60,
        verbose_name="Время на выполнение (секунд)"
    )
    # При установке привычку видят все пользователи.
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности"
    )
