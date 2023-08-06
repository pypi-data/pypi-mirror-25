# coding: utf-8
from django.core.exceptions import ImproperlyConfigured

_get_queryset_method_name = 'get_queryset'
_queryset_attribute_name = 'queryset'
_model_attribute_name = 'model'


def organization_view(view_cls):
    def wrapper():
        setattr(view_cls, _get_queryset_method_name, _create_organization_queryset_for_view(view_cls))
        return view_cls

    return wrapper()


def _create_organization_queryset_for_view(_view_cls):
    get_queryset = getattr(_view_cls, _get_queryset_method_name)
    queryset = getattr(_view_cls, _queryset_attribute_name)
    model = getattr(_view_cls, _model_attribute_name)

    get_organization_queryset = None

    if get_queryset is not None:
        def get_organization_queryset(self):
            _queryset = get_queryset(self)
            return _queryset.filter(organization=self.request.organization)

    elif queryset is not None:
        def get_organization_queryset(self):
            return queryset.filter(organization=self.request.organization)

    elif model is not None:
        def get_organization_queryset(self):
            default_org_asset_manager = getattr(model, 'org_objects')
            return default_org_asset_manager.get_queryset_for_organization(self.request.organization)

    if get_organization_queryset:
        return get_organization_queryset
    raise ImproperlyConfigured("View should contain at least one of the following attributes {}, {}, {}".format(
        _get_queryset_method_name,
        _queryset_attribute_name,
        _model_attribute_name,
    ))
