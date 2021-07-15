from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoAppConfig(AppConfig):
    name = 'commonknowledge.django'
    label = 'ckdjango'
    verbose_name = _("CK Django Helpers")
    default_auto_field = 'django.db.models.AutoField'
