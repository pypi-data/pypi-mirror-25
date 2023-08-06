# coding: utf-8
from djotali.contacts.templatetags.contacts_extras import format_number


def before_contact_saved(sender, instance, **kwargs):
    instance.phone_number = format_number(instance.phone_number).replace(' ', '')
