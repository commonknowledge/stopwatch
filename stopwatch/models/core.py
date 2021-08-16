from django.contrib.auth.models import AbstractUser
from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.documents.models import Document, AbstractDocument
from wagtail.snippets.models import register_snippet


class User(AbstractUser):
    pass


class StopwatchImage(AbstractImage):
    import_ref = models.CharField(max_length=1024, null=True, blank=True)

    admin_form_fields = Image.admin_form_fields


class StopwatchRendition(AbstractRendition):
    image = models.ForeignKey(
        StopwatchImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


class StopWatchDocument(AbstractDocument):
    import_ref = models.CharField(max_length=1024, null=True, blank=True)
    admin_form_fields = Document.admin_form_fields


@register_snippet
class Person(models.Model):
    name = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024)
    photo = models.ForeignKey(
        StopwatchImage, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)

    def __str__(self):
        return self.name


def pre_save_image_or_doc(sender, instance, *args, **kwargs):
    if instance.file is not None:
        if instance.file.name.startswith('import_'):
            instance.import_ref = instance.file.name


models.signals.pre_save.connect(pre_save_image_or_doc, sender=StopwatchImage)
models.signals.pre_save.connect(
    pre_save_image_or_doc, sender=StopWatchDocument)
