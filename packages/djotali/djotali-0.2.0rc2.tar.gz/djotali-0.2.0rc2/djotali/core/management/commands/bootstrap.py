import os

from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    _admin_username = 'admin@djotali.com'
    help = 'Bootstrap application'

    def handle(self, *args, **options):
        # Create the admin user for the platform
        # We get a default password only in dev environment, on other environment if pwd is not provided as env var, it will raise an exception
        pwd = os.getenv('ADMIN_PWD', 'changeme') if os.getenv('DEV') else os.getenv('ADMIN_PWD')
        if pwd is None:
            return
        if User.objects.filter(username=self._admin_username).exists():
            User.objects.get(username=self._admin_username).set_password(pwd)
        else:
            User.objects.create_superuser(self._admin_username, self._admin_username, pwd)
