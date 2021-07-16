from wagtail.core.models import Page
from commonknowledge.wagtail.models import ChildListMixin


class HomePage(ChildListMixin, Page):
    pass
