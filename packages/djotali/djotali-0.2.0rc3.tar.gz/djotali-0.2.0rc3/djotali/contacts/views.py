# coding: utf-8

import six
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from rest_framework import viewsets

from djotali.contacts.forms import ContactForm, ContactsGroupForm
from djotali.contacts.models import Contact, ContactsGroup, ContactSerializer
from djotali.core.views import paginate_in_context, RequestAwareFormViewMixin
from djotali.profile.decorators import organization_view


@organization_view
class IndexView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/index.html'
    context_object_name = 'contacts'
    paginate_by = 15
    paginate_orphans = 5
    ordering = ['last_name', 'first_name']

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context

    def get_queryset(self):
        return IndexView.build_queryset(self.request)

    @classmethod
    def build_queryset(cls, request):
        base_queryset = Contact.org_objects.get_queryset_for_organization(request.organization)
        querystring = request.GET.get('filter')

        if querystring:
            base_queryset = base_queryset.filter(
                Q(first_name__icontains=querystring) |
                Q(last_name__icontains=querystring) |
                Q(phone_number__icontains=querystring.replace(' ', ''))
            )
        ordering = IndexView.ordering
        if isinstance(ordering, six.string_types):
            ordering = (ordering,)
        base_queryset = base_queryset.order_by(*ordering)

        return base_queryset


@organization_view
class ContactsGroupsIndexView(LoginRequiredMixin, ListView):
    model = ContactsGroup
    template_name = 'contacts/groups_index.html'
    context_object_name = 'contacts_groups'
    paginate_by = 15
    ordering = ['-modified', 'name', 'contacts_count']

    def get_queryset(self):
        return ContactsGroupsIndexView.build_queryset()

    @classmethod
    def build_queryset(cls):
        ordering = ContactsGroupsIndexView.ordering
        if isinstance(ordering, six.string_types):
            ordering = (ordering,)
        return ContactsGroup.objects.order_by(*ordering).annotate(
            contacts_count=Count('contacts')
        )


@organization_view
class DeleteContactsGroupView(LoginRequiredMixin, DeleteView):
    model = ContactsGroup
    success_url = reverse_lazy('contacts:lists_index')
    template_name = 'contacts/groups_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        _object = self.get_object()

        self.object = _object
        context = self.get_context_data(object=_object, contacts_groups=ContactsGroupsIndexView.build_queryset())
        return self.render_to_response(context)

    def delete(self, request, *args, **kwargs):
        success_view = super(DeleteContactsGroupView, self).delete(request, args, kwargs)
        messages.add_message(self.request, messages.SUCCESS, "Contacts' group successfully deleted")
        return success_view


@organization_view
class EditContactsGroupView(RequestAwareFormViewMixin, LoginRequiredMixin, UpdateView):
    model = ContactsGroup
    form_class = ContactsGroupForm
    success_url = reverse_lazy('contacts-lists:index')
    template_name = 'contacts/groups_edit.html'

    def form_valid(self, form):
        valid = super(EditContactsGroupView, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Contacts' group successfully edited")
        return valid


@organization_view
class EditContactView(RequestAwareFormViewMixin, LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contacts:index')
    template_name = 'contacts/edit.html'

    def form_valid(self, form):
        valid = super(EditContactView, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Contact successfully edited")
        return valid

    def get_success_url(self):
        default_success_url = super(EditContactView, self).get_success_url()
        success_url = self.request.GET.get('success_url')
        return success_url if success_url else default_success_url


@organization_view
class CreateContactView(RequestAwareFormViewMixin, LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy('contacts:index')
    template_name = 'contacts/new.html'

    def form_valid(self, form):
        valid = super(CreateContactView, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Contact successfully created")
        return valid


@organization_view
class DeleteContactView(LoginRequiredMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('contacts:index')
    template_name = 'contacts/confirm_delete.html'

    def get(self, request, *args, **kwargs):
        _object = self.get_object()

        self.object = _object
        context = self.get_context_data(object=_object, contacts=IndexView.build_queryset(self.request))
        return self.render_to_response(context)

    def delete(self, request, *args, **kwargs):
        success_view = super(DeleteContactView, self).delete(request, args, kwargs)
        messages.add_message(self.request, messages.SUCCESS, "Contact successfully deleted")
        return success_view

    def get_success_url(self):
        default_success_url = super(DeleteContactView, self).get_success_url()
        success_url = self.request.GET.get('success_url')
        return success_url if success_url else default_success_url


@organization_view
class ShowContactsGroupView(LoginRequiredMixin, DetailView):
    template_name = "contacts/groups_show.html"
    model = ContactsGroup
    context_object_name = 'contacts_group'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Related contacts
        paginate_in_context(self.request, self.object.contacts, context, "contacts", 5)

        context["avoid_deleting_contact"] = True

        return context


@organization_view
class CreateContactsGroupsView(RequestAwareFormViewMixin, LoginRequiredMixin, CreateView):
    model = ContactsGroup
    template_name = "contacts/groups_new.html"
    form_class = ContactsGroupForm


class ContactsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get_queryset(self):
        request = self.request
        return IndexView.build_queryset(request)


class ContactsGroupsContactsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    pagination_class = None

    # TODO un petit decorator pour aider à récupérer les arguments dans l'url plus simplement
    def get_queryset(self):
        request = self.request
        contacts_group_id = request.parser_context['kwargs']['group_id']
        return get_object_or_404(ContactsGroup, pk=contacts_group_id, organization=request.organization).contacts
