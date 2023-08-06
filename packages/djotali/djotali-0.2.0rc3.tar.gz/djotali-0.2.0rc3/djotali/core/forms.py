# coding: utf-8
from django.forms import ModelForm


class BaseForm(ModelForm):
    required_css_class = 'form-group'

    def __init__(self, *args, **kwargs):
        if "request" in kwargs:
            setattr(self, "request", kwargs.pop("request"))
        super(BaseForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if hasattr(self, 'request'):
            self.instance.organization = self.request.organization
        return super().save(commit)
