# coding: utf-8
from allauth.account.models import EmailAddress, EmailConfirmation
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from organizations.models import Organization

from djotali.campaigns.models import Campaign
from djotali.contacts.models import Contact, ContactsGroup
from djotali.core.seed.factories import ContactsGroupFactory, CampaignFactory, OrganizationFactory, ContactFactory


class Command(BaseCommand):
    help = 'Seed Database'

    def handle(self, *args, **options):
        with transaction.atomic():
            try:
                # Drop All first
                self.stdout.write(self.style.WARNING('Truncating tables first...'))
                Organization.objects.all().delete()
                User.objects.all().delete()
                EmailAddress.objects.all().delete()
                EmailConfirmation.objects.all().delete()
                ContactsGroup.objects.all().delete()
                Contact.objects.all().delete()
                Campaign.objects.all().delete()

                OrganizationFactory.create_batch(3)

                contacts = ContactFactory.create_batch(250)
                for _ in range(12):
                    ContactsGroupFactory.create(contacts=contacts)
                CampaignFactory.create_batch(15)

                call_command('bootstrap')
                self.stdout.write(self.style.SUCCESS('Database seeded'))
            except CommandError as e:
                self.stdout.write(self.style.ERROR('Failed to seed database. Rolling back transaction', e))
