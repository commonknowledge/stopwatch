from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BootstrapAppConfig(AppConfig):
    name = 'commonknowledge.bootstrap'
    label = 'ckbootstrap'
    verbose_name = _("CK Bootstrap Helpers")
    default_auto_field = 'django.db.models.AutoField'
