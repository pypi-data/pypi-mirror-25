# coding: utf-8
import datetime
import random

import factory
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.db.models import signals
from django.utils import timezone
from django.utils.text import slugify
from faker import Faker
from organizations.models import Organization

import djotali.campaigns.models as campaigns_models
import djotali.contacts.models as contacts_models

faker = Faker('fr_FR')


class OrganizationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker('company')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))

    @factory.post_generation
    def create_organization_users(self, create, extracted, **kwargs):
        if not create:
            return

        organization_users = UserFactory.create_batch(5)
        # So that organization's admin user is always an active user
        # The organization's admin user is the first user of the organization
        organization_users = sorted(organization_users, key=lambda user: 0 if user.is_active else 1)
        for organization_user in organization_users:
            self.add_user(organization_user)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.LazyAttribute(lambda u: u.email)
    is_active = factory.Faker('boolean', chance_of_getting_true=80)
    password = factory.PostGenerationMethodCall('set_password', 'changeme')

    @factory.post_generation
    def make_email(self, create, extracted, **kwargs):
        EmailAddress(email=self.email, user_id=self.id).save()


class CampaignFactory(factory.DjangoModelFactory):
    class Meta:
        model = campaigns_models.Campaign

    message = factory.Faker('text', max_nb_chars=140)

    @factory.lazy_attribute
    def name(self):
        return "{}% Off ! {}".format(
            factory.Faker('random_int', min=20, max=85).generate({}),
            factory.Faker('sentence', nb_words=2).generate({})
        )

    @factory.lazy_attribute
    def start_date(self):
        return timezone.now() + random.choice([-2, 2]) * datetime.timedelta(days=random.choice(range(0, 10)))

    contacts_group = factory.Iterator(contacts_models.ContactsGroup.objects.all())
    organization = factory.LazyAttribute(lambda c: c.contacts_group.organization)

    @factory.post_generation
    def make_notifications(self, create, extracted, **kwargs):
        if not create:
            return

        if self.contacts_group.contacts:
            for contact in self.contacts_group.contacts.all():
                n = NotificationFactory.create(contact=contact, campaign=self, status=0, organization=self.organization)
                self.notifications.add(n)


class ContactsGroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = contacts_models.ContactsGroup

    name = factory.Faker('company')
    # TODO Do a mix
    is_removed = False
    organization = factory.Iterator(Organization.objects.all())

    @factory.post_generation
    def contacts(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        organization_contacts = [contact for contact in extracted if contact.organization == self.organization]
        group_contacts = random.choices(organization_contacts, k=random.randint(5, len(organization_contacts)))
        for contact in group_contacts:
            self.contacts.add(contact)


@factory.django.mute_signals(signals.pre_save, signals.post_save)
class ContactFactory(factory.DjangoModelFactory):
    class Meta:
        model = contacts_models.Contact

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone_number = factory.Faker('senegal_phone_number')
    # TODO Do a mix
    is_removed = False
    organization = factory.Iterator(Organization.objects.all())


class NotificationFactory(factory.DjangoModelFactory):
    class Meta:
        model = campaigns_models.Notification

    campaign = factory.Iterator(campaigns_models.Campaign.objects.all())
    contact = factory.Iterator(contacts_models.Contact.objects.all())
    status = random.choice([0, 1, -1])
    organization = factory.Iterator(Organization.objects.all())
