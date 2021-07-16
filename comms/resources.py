from stopwatch.models import StopWatchDocument, StopwatchImage
from import_export import resources, widgets, fields

from comms import models


class ImageWidget(widgets.Widget):
    def clean(self, value: str, row=None, *args, **kwargs):
        if not value:
            return

        if value.lower().endswith('.pdf'):
            return StopWatchDocument.objects.get(import_ref=value)
        else:
            return StopwatchImage.objects.get(import_ref=value)

    def render(self, value, obj=None):
        if not value:
            return

        try:
            return value.file.url
        except NotImplementedError:
            pass


class NewsItemResource(resources.ModelResource):
    class Meta:
        model = models.NewsItem
        fields = ('import_ref', 'title',
                  'intro_text', 'content', 'photo')
        import_id_fields = ('import_ref',)

    photo = fields.Field(widget=ImageWidget(),
                         attribute='photo', column_name='photo')

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.parent = parent

    def before_save_instance(self, instance, using_transactions, dry_run):
        self.parent.add_child(instance=instance)

    def import_field(self, field, obj, data, *args):
        if field.column_name != 'parent':
            return super().import_field(field, obj, data, *args)
