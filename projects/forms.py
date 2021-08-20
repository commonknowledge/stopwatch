from commonknowledge.wagtail.models import SortOption
from stopwatch.models.pages import Category
from django_bootstrap5.widgets import RadioSelectButtonGroup
from django import forms


class EventFilterForm(forms.Form):
    query = forms.CharField(required=False)
    theme = forms.ChoiceField(required=False)

    def __init__(self, themes, **kwargs):
        super().__init__(**kwargs)

        self.fields['theme'].choices = tuple(
            (theme.slug, theme.title)
            for theme in themes
        )
