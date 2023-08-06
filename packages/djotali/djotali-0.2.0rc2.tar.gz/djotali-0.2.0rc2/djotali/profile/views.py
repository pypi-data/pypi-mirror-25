# Create your views here.
from allauth.account.forms import SignupForm
from allauth.account.utils import complete_signup
from allauth.account.views import RedirectAuthenticatedUserMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import View
from organizations.models import Organization
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from djotali.core.views import ViewUtilsMixin
from djotali.profile.core import InvitationTokenGenerator
from djotali.profile.models import OrganizationSerializer


class OrganizationAdminViewMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        request = self.request
        return request.organization.is_admin(request.user)


class InvitationView(RedirectAuthenticatedUserMixin, View):
    http_method_names = ['get', 'post']
    redirect_field_name = 'next'

    def get_success_url(self):
        from allauth import app_settings as global_app_settings
        return global_app_settings.LOGIN_REDIRECT_URL

    def get(self, request):
        return render(request, 'profile/invitation.html', context={
            'email': request.GET['email'],
            'organization': request.GET['organization'],
            'token': request.GET['token'],
        })

    def post(self, request):
        from allauth import app_settings as global_app_settings
        signup_form = SignupForm(request.POST)
        signup_form.full_clean()
        if not signup_form.is_valid():
            # If form is invalid, it is certainly because of an invalid token
            return render(request, 'profile/invitation.html', context={
                'email': request.POST['email'],
                'organization': request.POST['organization'],
                'token': request.POST['token'],
                'errors': ["Votre invitation n'est pas/plus valide, veuillez recontacter votre administrateur pour en recréer une."]
            })

        user = signup_form.save(request)
        if user is None:
            return HttpResponseBadRequest()
        from allauth.account import app_settings
        return complete_signup(request, user, app_settings.EMAIL_VERIFICATION, global_app_settings.LOGIN_REDIRECT_URL)


class InviteOrganizationUserView(ViewUtilsMixin, LoginRequiredMixin, OrganizationAdminViewMixin, View):
    http_method_names = ['post']
    subject_template = "profile/invitation_email_subject.txt"
    body_template = "profile/invitation_email_body.html"

    def __init__(self):
        super(InviteOrganizationUserView, self).__init__()
        self.invitation_token_generator = InvitationTokenGenerator()
        self.subject_template = loader.get_template(self.subject_template)
        self.body_template = loader.get_template(self.body_template)

    def post(self, request):
        post_dict = self._get_post_dict(request)
        email_to_invite = post_dict["email"]
        organization = request.organization.name

        token = self.invitation_token_generator.generate_token(email_to_invite, organization)
        signup_path = '{}?token={}&email={}&organization={}'.format(reverse('profile:invitation'), token, email_to_invite, organization)
        invitation_url = request.build_absolute_uri(signup_path)

        subject = self.subject_template.render({
            'organization': organization,
        }).strip()

        body = self.body_template.render({
            'organization': organization,
            'invitation_url': invitation_url,
        })

        send_mail(
            subject,
            body,
            'contact@djotali.com',
            [email_to_invite],
            fail_silently=False,
        )
        return HttpResponseRedirect(reverse('profile:organization-users'))


class OrganizationsView(RetrieveAPIView):
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        return [AllowAny()]

    def get_object(self):
        organization_name = self.kwargs.get('organization_name')
        return get_object_or_404(Organization, name__iexact=organization_name)


class ActivateOrganizationUsersView(ViewUtilsMixin, LoginRequiredMixin, OrganizationAdminViewMixin, View):
    http_method_names = ['post']
    _activate_checkbox_prefix = 'activate_'

    def post(self, request):
        # We need this for deactivated users as the inputs
        organization_users = _get_organization_users(request.organization.id, request.user.id)
        post_dict = self._get_post_dict(request)
        updated_users = [
            (user.id, self._is_active(user.id, post_dict))
            for user in organization_users
            if self._has_user_active_state_changed(user, post_dict)]

        user_ids_to_activate = [updated_user[0] for updated_user in updated_users if updated_user[1]]
        # built-in bulk update http://voorloopnul.com/blog/doing-bulk-update-and-bulk-create-with-django-orm/
        User.objects.filter(id__in=user_ids_to_activate).update(is_active=True)

        user_ids_to_deactivate = [updated_user[0] for updated_user in updated_users if not updated_user[1]]
        # built-in bulk update http://voorloopnul.com/blog/doing-bulk-update-and-bulk-create-with-django-orm/
        User.objects.filter(id__in=user_ids_to_deactivate).update(is_active=False)

        # Redirect to avoid unintentional submission if the user tries to reload its page on his browser
        return HttpResponseRedirect(reverse('profile:organization-users'))

    def _get_user_ids_for_state(self, request, state):
        post_dict = self._get_post_dict(request)
        return [
            int(key[len(self._activate_checkbox_prefix):])
            for key in post_dict.keys()
            if self._activate_checkbox_prefix in key and post_dict[key] == state]

    @classmethod
    def _has_user_active_state_changed(cls, user, post_dict):
        return user.is_active != cls._is_active(user.id, post_dict)

    @classmethod
    def _is_active(cls, user_id, post_dict):
        return (cls._activate_checkbox_prefix + str(user_id)) in post_dict


class OrganizationUsersView(LoginRequiredMixin, OrganizationAdminViewMixin, View):
    http_method_names = ['get']

    def get(self, request):
        context = {
            'users': _get_organization_users(request.organization.id, request.user.id)
        }
        return render(request, 'profile/organization_users.html', context=context)


def _get_organization_users(organization_id, current_user_id):
    return User.objects.filter(organizations_organization__id=organization_id).exclude(id=current_user_id)
