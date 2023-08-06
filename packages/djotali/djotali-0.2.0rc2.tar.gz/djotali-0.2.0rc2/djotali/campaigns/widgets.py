# coding: utf-8
from django.urls import reverse

from djotali.core.widgets import BoundModelsSelectWidget


class CampaignContactsGroupBoundModelsSelectWidget(BoundModelsSelectWidget):
    def get_url(self, value):
        if value is None:
            return None
        return reverse('contacts-groups:edit', args=(value,))

    def get_label(self):
        return "Editer le groupe de contacts actuel"
