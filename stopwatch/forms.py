from commonknowledge.wagtail.models import SortOption
from stopwatch.models.pages import Category
from django_bootstrap5.widgets import RadioSelectButtonGroup
from django import forms


class RadioSelectButton(forms.RadioSelect):
    """A RadioSelect that renders as a horizontal button groep."""

    template_name = "django_bootstrap5/widgets/radio_select.html"


class CategoryFilterForm(forms.Form):
    query = forms.CharField(required=False)
    sort = forms.ChoiceField(
        choices=SortOption.to_field_choices(Category.sort_options),
        required=False
    )
    theme = forms.ChoiceField(required=False, widget=RadioSelectButton)

    def __init__(self, tags, **kwargs):
        super().__init__(**kwargs)

        self.fields['theme'].choices = tuple(
            (tag.slug, tag.name)
            for tag in tags
        )
