# coding: utf-8


def profile_context_processor(request):
    is_organization_admin = request.is_organization_admin if hasattr(request, 'is_organization_admin') else None
    return {
        "profile_is_organization_admin": is_organization_admin,
    }
