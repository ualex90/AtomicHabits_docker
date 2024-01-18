from django.core.management import BaseCommand

from app_users.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-l', '--tg', type=str, help='Telegram ID')

    def handle(self, *args, **kwargs):
        tg_id = kwargs.get('tg') if kwargs.get('tg') else '000000000'
        email = 'admin@sky.pro'
        password = 'admin'

        user = User.objects.create(
            email=email,
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            telegram_id=tg_id
        )

        user.set_password(password)
        user.save()
        print(f'email: {email}\npassword: {password}\nTelegram ID: {tg_id}')
