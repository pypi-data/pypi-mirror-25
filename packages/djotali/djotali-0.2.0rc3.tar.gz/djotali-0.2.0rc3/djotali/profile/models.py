# Create your models here.
from django.db import models
from model_utils.managers import SoftDeletableManager
from organizations.models import Organization
from rest_framework import serializers


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('name',)


class OrganizationAssetManager(SoftDeletableManager):
    def get_queryset_for_organization(self, organization):
        return super(OrganizationAssetManager, self).get_queryset().filter(organization_id=organization.id)


class AbstractOrganizationAsset(models.Model):
    organization = models.ForeignKey('organizations.Organization')

    org_objects = OrganizationAssetManager()

    class Meta:
        abstract = True
