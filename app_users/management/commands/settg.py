from django.core.management import BaseCommand

from app_users.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-l', '--tg', type=str, help='Telegram ID')

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        password = '123qwe'
        tg_id = kwargs.get('tg') if kwargs.get('tg') else '000000000'

        for user in users:
            user.telegram_id = tg_id
            user.set_password(password)
            user.save()
            print(
                f'email: {user.email}; '
                f'password: {password}; '
                f'Telegram ID: {tg_id}'
                f'{"; модератор" if user.is_staff else ""}'
            )
