from commonknowledge.wagtail.models import SortOption
from stopwatch.models.pages import Category
from django_bootstrap5.widgets import RadioSelectButtonGroup
from django import forms
from django.contrib.contenttypes.models import ContentType
from wagtail.models import Page


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

    def __init__(self, tags=list(), **kwargs):
        super().__init__(**kwargs)

        self.fields['theme'].choices = tuple(
            (tag.slug, tag.name)
            for tag in tags
        )


class AgingPagesFilterForm(forms.Form):
  
    first_published_before = forms.DateField(
        required=False,
       widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        ),
        label="First Published Before",
    )
    status = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All'),
            ('live', 'Live'),
            ('draft', 'Draft'),
        ],
        label="Status",
    )
    page_type = forms.ChoiceField(
        required=False,
        choices=[], 
        label="Page Type",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        content_types = ContentType.objects.filter(id__in=Page.objects.values('content_type_id')).distinct()
        self.fields['page_type'].choices = [('', 'All')] + [
            (ct.model, ct.name.capitalize()) for ct in content_types
        ]
