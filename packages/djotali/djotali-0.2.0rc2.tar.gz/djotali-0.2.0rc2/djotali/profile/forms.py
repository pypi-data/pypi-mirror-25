from django.core.exceptions import ValidationError
from django.forms.forms import Form
from organizations.models import Organization

from djotali.profile.core import InvitationTokenGenerator


class SignupWithOrganizationForm(Form):
    invitation_token_generator = InvitationTokenGenerator()

    def clean(self):
        self._validate_token_if_organization_exist(self.data)
        return super(SignupWithOrganizationForm, self).clean()

    @classmethod
    def _validate_token_if_organization_exist(cls, data):
        organization_name = data['organization']
        if Organization.objects.filter(name=organization_name).exists():
            token = data['token']
            email = data['email']
            if not cls.invitation_token_generator.check_token(token, email, organization_name):
                raise ValidationError("L'inscription sur une entreprise ne peut se faire sans l'aval de son administrateur.")

    def signup(self, request, user):
        # We get or create the organization when everything is OK and add the user to it
        # The first user is the admin
        from organizations.models import Organization
        organization_name = request.POST['organization']
        organization, created = Organization.objects.get_or_create(name=organization_name)
        organization.add_user(user)
        organization.save()
