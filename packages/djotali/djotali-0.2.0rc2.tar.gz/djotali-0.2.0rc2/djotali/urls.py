# coding: utf-8
"""djotali URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from djotali.contacts.views import ContactsViewSet, ContactsGroupsContactsViewSet
from djotali.profile.views import OrganizationsView

router = routers.DefaultRouter()
router.register(r'contacts', ContactsViewSet)
router.register(r'contacts-groups/(?P<group_id>\d+)/contacts', ContactsGroupsContactsViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^core/', include('djotali.core.urls')),
    url(r'^dashboard/', include('djotali.dashboard.urls')),
    url(r'^contacts/', include('djotali.contacts.urls')),
    url(r'^contacts-groups/', include('djotali.contacts.groups_urls')),
    url(r'^login/', TemplateView.as_view(template_name='core/login.html')),
    url(r'^campaigns/', include('djotali.campaigns.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/', include('djotali.profile.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api/organizations/(?P<organization_name>[\S ]+)', OrganizationsView.as_view()),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token-auth/', obtain_jwt_token),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
