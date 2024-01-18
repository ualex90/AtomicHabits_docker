from django.core.management import BaseCommand

from app_users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = 'admin@sky.pro'
        password = 'admin'

        admin = User.objects.get(email=email)
        admin.set_password(password)
        admin.save()
        print(f'email: {email}\npassword: {password}')
