# coding: utf-8
from django.conf import settings


def settings_context_processor(request):
    return {
        "settings_vue_lib": settings.VUE_LIB,
        "settings_vuex_lib": settings.VUEX_LIB,
        "settings_axios_lib": settings.AXIOS_LIB,
    }
