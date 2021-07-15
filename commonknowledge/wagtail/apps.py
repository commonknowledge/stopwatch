from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailAppConfig(AppConfig):
    name = 'commonknowledge.wagtail'
    label = 'ckwagtail'
    verbose_name = _("CK Wagtail Helpers")
    default_auto_field = 'django.db.models.AutoField'
