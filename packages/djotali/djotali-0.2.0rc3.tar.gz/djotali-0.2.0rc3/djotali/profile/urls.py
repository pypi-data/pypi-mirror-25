# coding: utf-8
from django.conf.urls import url

from djotali.profile import views

app_name = 'profile'
urlpatterns = [
    url(r'^organization-users$', views.OrganizationUsersView.as_view(), name='organization-users'),
    url(r'^activate-users$', views.ActivateOrganizationUsersView.as_view(), name='activate-users'),
    url(r'^invite-users$', views.InviteOrganizationUserView.as_view(), name='invite-users'),
    url(r'^invitation$', views.InvitationView.as_view(), name='invitation'),
]
