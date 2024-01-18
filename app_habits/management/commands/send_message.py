from django.core.management import BaseCommand

from app_habits.tasks import send_message_tg, print_task


class Command(BaseCommand):

    def handle(self, *args, **options):
        # print_task.delay()
        send_message_tg.delay(
            telegram_id='361991641',
            task="Test task"
        )
