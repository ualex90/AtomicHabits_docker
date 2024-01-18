import json
from datetime import datetime, date, time, timedelta

import requests
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from app_habits.models import Habit
from config import settings


class TgBot:
    URL = "https://api.telegram.org/bot"
    TOKEN = settings.TELEGRAM_BOT_TOKEN

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def send_message(self, text):
        requests.post(
            url=f'{self.URL}{self.TOKEN}/sendMessage',
            data={
                'chat_id': self.chat_id,
                'text': text
            }
        )


def get_schedule(habit: Habit):
    """ Получение периода выполнения задачи """

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=int(habit.periodicity),
        # period=IntervalSchedule.MINUTES,  Для проверки работоспособности
        period=IntervalSchedule.DAYS,
    )
    return schedule


def add_task(habit: Habit):
    """ Создание периодической задачи для напоминания о полезной привычке """

    # Создание или получение имеющегося периода
    schedule = get_schedule(habit)

    # Создание задачи
    PeriodicTask.objects.create(
        name=f'{habit.id}: {habit.task}',
        task='app_habits.tasks.send_message_tg',
        interval=schedule,
        kwargs=json.dumps(
            {
                'telegram_id': habit.owner.telegram_id,
                'start_time': time.strftime(habit.start_time, '%H:%M'),
                'task': habit.task,
                'location': habit.location,
                'time_to_complete': habit.time_to_complete,
                'reward': habit.reward,
                'related_habit': {
                    'task': habit.related_habit.task,
                    'location': habit.related_habit.location,
                    'time_to_complete': habit.related_habit.time_to_complete,
                } if habit.related_habit else None,
            }, ensure_ascii=False
        ),
        # Отправляем напоминание за 5 минут до начала действия
        start_time=datetime.combine(date.today(), habit.start_time) - timedelta(minutes=5),
    )


def update_task(habit: Habit):
    """ Обновление периодической задачи """

    # Ищем периодическую задачу и если она существует, изменяем ее
    if task_qs := PeriodicTask.objects.filter(name=f'{habit.id}: {habit.task}'):
        task = task_qs[0]
        # Создание или получение имеющегося периода
        schedule = get_schedule(habit)

        # Изменение задачи
        task.name = f'{habit.id}: {habit.task}'
        task.interval = schedule
        task.kwargs = json.dumps(
            {
                'telegram_id': habit.owner.telegram_id,
                'start_time': time.strftime(habit.start_time, '%H:%M'),
                'task': habit.task,
                'location': habit.location,
                'time_to_complete': habit.time_to_complete,
                'reward': habit.reward,
                'related_habit': {
                    'task': habit.related_habit.task,
                    'location': habit.related_habit.location,
                    'time_to_complete': habit.related_habit.time_to_complete,
                } if habit.related_habit else None,
            }, ensure_ascii=False
        )
        task.start_time = datetime.combine(date.today(), habit.start_time) - timedelta(minutes=5)
        task.save()


def delete_task(habit: Habit):
    """ Обновление периодической задачи """

    # Ищем периодическую задачу и если она существует, удалим ее
    if task_qs := PeriodicTask.objects.filter(name=f'{habit.id}: {habit.task}'):
        task = task_qs[0]
        task.delete()


def send_message_to_telegram(**kwargs):
    """ Отправка сообщения """

    chat_id = kwargs.get('telegram_id')
    start_time = kwargs.get("start_time")
    task = kwargs.get("task")
    location = kwargs.get("location")
    time_to_complete = kwargs.get("time_to_complete")
    reward = kwargs.get("reward")
    related_habit = kwargs.get("related_habit")

    # Формирование основного текста
    text = (
        f'Я буду {task} в {start_time} {location} '
        f'в течении {time_to_complete} секунд.'
    )
    # Формирование текста вознаграждения при наличии
    reward = f'\nЗа это, я {reward}.' if reward else ''
    # Формирование текста связанной привычки при наличии
    related_habit = (f'\nПосле этого я {related_habit.get("task")}'
                     f' {related_habit.get("location")} '
                     f'в течении {related_habit.get("time_to_complete")} секунд.') if related_habit else ''
    # Отправка сообщения
    tg_bot = TgBot(chat_id)
    message = text + reward + related_habit
    tg_bot.send_message(message)

    # Для тестирования добавляем возврат сформированного сообщения
    return message
