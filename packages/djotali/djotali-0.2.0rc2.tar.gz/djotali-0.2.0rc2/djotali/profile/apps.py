from allauth.account.signals import user_signed_up
from django.apps import AppConfig


class ProfileConfig(AppConfig):
    name = 'djotali.profile'

    def ready(self):
        from djotali.profile.signals import alert_admin
        user_signed_up.connect(alert_admin)
