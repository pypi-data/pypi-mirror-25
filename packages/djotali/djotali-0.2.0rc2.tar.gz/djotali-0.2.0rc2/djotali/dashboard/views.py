# coding: utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from djotali.campaigns.models import Campaign, Notification
from djotali.contacts.models import Contact
from djotali.core.utils import is_celery_running


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        organization = self.request.organization
        context['total_campaings'] = Campaign.org_objects.get_queryset_for_organization(organization).count()
        context['total_contacts'] = Contact.org_objects.get_queryset_for_organization(organization).count()
        context['is_broker_running'] = is_celery_running()
        context['total_messages'] = Notification.org_objects.get_queryset_for_organization(organization).filter(status=1).count()
        context['campaigns'] = Campaign.org_objects.get_queryset_for_organization(organization).all()[:5]
        return context
