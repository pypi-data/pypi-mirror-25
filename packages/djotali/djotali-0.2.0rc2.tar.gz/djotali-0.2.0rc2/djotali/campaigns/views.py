# coding: utf-8
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Sum
from django.db.models.expressions import Case, When
from django.db.models.fields import IntegerField
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views import generic

from djotali.campaigns.forms import CampaignForm
from djotali.campaigns.models import Campaign, Notification
from djotali.campaigns.tasks import notify_campaign, notify_task, is_campaign_launched
from djotali.contacts.models import ContactsGroup
from djotali.core.utils import is_celery_running
from djotali.core.views import paginate_in_context, RequestAwareFormViewMixin
from djotali.profile.decorators import organization_view


@organization_view
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'campaigns/index.html'
    context_object_name = "list_objects"
    paginate_by = 5
    queryset = Campaign.get_closest_campaigns_query_set()


@organization_view
class NotificationsView(LoginRequiredMixin, generic.DetailView):
    model = Campaign
    template_name = 'campaigns/notifications.html'
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        context = super(NotificationsView, self).get_context_data(**kwargs)
        campaign = self.object

        status = self.request.GET.get('status')
        context["status"] = status

        notifications = campaign.notifications
        if status is not None:
            notifications = notifications.filter(status=Notification.get_status_value(status))
        paginate_in_context(self.request, notifications, context, "notifications")

        context['editable'] = not is_campaign_launched(campaign.id)

        return context


@organization_view
class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Campaign
    template_name = 'campaigns/show.html'
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        broker_running = is_celery_running()

        if not broker_running:
            messages.add_message(self.request, messages.ERROR, "Broker is not running.")
        c = self.object

        context['is_broker_running'] = broker_running

        context['total_notifications'] = c.notifications.count()
        context['editable'] = not is_campaign_launched(c.id)

        return context

    def get_queryset(self):
        return super(DetailView, self).get_queryset(). \
            prefetch_related('notifications__contact'). \
            annotate(
            failed=Sum(
                Case(
                    When(notifications__status=-1, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            sent=Sum(
                Case(
                    When(notifications__status=1, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            progress=Sum(
                Case(
                    When(notifications__status=0, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )


@organization_view
class CreateView(RequestAwareFormViewMixin, LoginRequiredMixin, generic.CreateView):
    model = Campaign
    template_name = 'campaigns/new.html'
    form_class = CampaignForm

    def get_success_url(self):
        return reverse('campaigns:show', args=[self.object.id])

    def get_form_kwargs(self):
        form_kwargs = super(CreateView, self).get_form_kwargs()
        form_kwargs.update({
            'request': self.request
        })
        return form_kwargs

    def form_valid(self, form):
        response = super(CreateView, self).form_valid(form)

        # We create notifications associated to contacts
        notifications = []
        organization = self.request.organization
        for contact in ContactsGroup.get_contacts_queryset(self.object.contacts_group, organization).all():
            notifications.append(Notification(contact=contact, campaign=self.object, status=0, organization=organization))
        Notification.objects.bulk_create(notifications)

        return response


@organization_view
class EditView(RequestAwareFormViewMixin, LoginRequiredMixin, generic.UpdateView):
    model = Campaign
    template_name = 'campaigns/edit.html'
    form_class = CampaignForm

    def get_success_url(self):
        return reverse('campaigns:show', args=[self.object.id])

    def get_form_kwargs(self):
        form_kwargs = super(EditView, self).get_form_kwargs()
        form_kwargs.update({
            'request': self.request
        })
        return form_kwargs


@login_required
def campaign_notify(request, campaign_id):
    broker_running = is_celery_running()

    if broker_running:
        notify_campaign.delay(campaign_id)

    return HttpResponseRedirect(reverse('campaigns:show', args=(campaign_id,)))


@login_required
def notify(request, campaign_id, notification_id):
    broker_running = is_celery_running()

    if broker_running:
        messages.add_message(request, messages.SUCCESS, "Processing Notification %s !" % notification_id)
        notify_task.delay(campaign_id, notification_id)
    else:
        messages.add_message(request, messages.ERROR, "Oops ! Broker is not running !")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
