# coding: utf-8
from django.utils.deprecation import MiddlewareMixin
from organizations.models import Organization


class OrganizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if not user or not user.id:
            return
        organization = request.session.get('organization')
        is_organization_admin = request.session.get('is_organization_admin')
        if user.is_staff:
            # The admin has the ability to impersonate an organization
            organization, is_organization_admin = self._impersonate_organization_if_requested_from_admin(request, user, organization, is_organization_admin)
        else:
            if organization is None or is_organization_admin:
                # A user has one and only one organization that is created on signup
                organization = Organization.active.filter(users__id=user.id)[0]
                is_organization_admin = organization.is_admin(user)
        request.session['organization'] = organization
        request.session['is_organization_admin'] = is_organization_admin
        request.organization = organization
        request.is_organization_admin = is_organization_admin

    @staticmethod
    def _impersonate_organization_if_requested_from_admin(request, user, organization, is_organization_admin):
        if 'admin_org' in request.GET:
            admin_organization_id = request.GET['admin_org']
            organization = Organization.active.get(id=admin_organization_id)
            if not organization.is_admin(user):
                # If admin was not yet part of the organization, we add him
                organization.add_user(user, is_admin=True)
            is_organization_admin = True
        return organization, is_organization_admin
