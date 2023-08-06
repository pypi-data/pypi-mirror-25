from django.contrib.auth.models import User
from django.template import loader
from django.urls import reverse
from organizations.models import OrganizationOwner

_subject_template = "profile/new_signup_email_subject.txt"
_body_template = "profile/new_signup_email_body.html"


def alert_admin(request, user, **kwargs):
    # Important to import locally or it won't be mocked
    from django.core.mail import send_mail
    organization_name = request.POST['organization']
    owner = OrganizationOwner.objects.get(organization__name__iexact=organization_name)
    organization_owner_user = User.objects.get(
        organizations_organizationuser__id=owner.organization_user.id,
    )
    # Username is the user's email in our current flow
    owner_email = organization_owner_user.username

    subject_template = loader.get_template(_subject_template)
    subject = subject_template.render({
        'organization': organization_name,
    })

    body_template = loader.get_template(_body_template)
    body = body_template.render({
        # Username is the user's email in our current flow
        'signup_email': user.username,
        'organization': organization_name,
        'activate_url': reverse('profile:activate-users'),
    })

    send_mail(
        subject,
        body,
        'contact@djotali.com',
        [owner_email],
        fail_silently=False,
    )
