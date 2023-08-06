# coding: utf-8

from django.apps import AppConfig
from django.db.models.signals import post_save


class CampaignsConfig(AppConfig):
    name = 'djotali.campaigns'

    def ready(self):
        from djotali.campaigns.signals import update_notifications_after_contact_save
        post_save.connect(update_notifications_after_contact_save, sender='contacts.Contact')
