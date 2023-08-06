# coding: utf-8
from django.apps import AppConfig
from django.db.models.signals import pre_save


class ContactsConfig(AppConfig):
    name = 'djotali.contacts'

    def ready(self):
        from djotali.contacts.signals import before_contact_saved
        pre_save.connect(before_contact_saved, sender='contacts.Contact')
