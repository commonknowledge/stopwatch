from django.contrib.auth.models import AbstractUser
from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.documents.models import Document, AbstractDocument
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


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
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True)
    twitter = models.CharField(max_length=128, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs) -> None:
        if self.twitter is not None:
            self.twitter = self.twitter.lstrip('@').strip()
        return super().save(*args, **kwargs)

    panels = [
        FieldPanel('name'),
        FieldPanel('title'),
        ImageChooserPanel('photo'),
        FieldPanel('bio'),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('twitter'),
            FieldPanel('website'),
        ], 'Contact Details')
    ]

    def __str__(self):
        return self.name


@register_setting
class SiteSettings(BaseSetting):
    facebook = models.URLField(
        null=True,
        blank=True,
        help_text='Your Facebook page URL')
    instagram = models.CharField(
        null=True,
        blank=True,
        max_length=255, help_text='Your Instagram username, without the @')
    twitter = models.CharField(
        null=True,
        blank=True,
        max_length=255, help_text='Your Twitter username, without the @')
    youtube = models.URLField(
        null=True,
        blank=True,
        help_text='Your YouTube channel or user account URL')

    standard_donation_request = RichTextField(
        default='We aim to address excess and disproportionate stop and search, promote best practice and ensure fair, effective policing for all.')
    standard_mailinglist_request = RichTextField(
        default='Regular updates on our activities, noteworthy articles, and how you can get involved in our work.')

    donation_page = models.ForeignKey(
        Page,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    tagline = RichTextField(
        default="",
        help_text='Text displayed at the base of a site')
    tagline_long = RichTextField(
        default="<strong>StopWatch</strong> is a coalition of legal experts, academics, citizens and civil liberties campaigners. We aim to address excess and disproportionate stop and search, promote best practice and ensure fair, effective policing for all.",
        help_text='Text displayed at the base of pages')

    panels = [
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('instagram'),
            FieldPanel('twitter'),
            FieldPanel('youtube')
        ], 'Social'),

        MultiFieldPanel([
            PageChooserPanel('donation_page'),
        ], 'Special pages'),

        MultiFieldPanel([
            FieldPanel('tagline'),
            FieldPanel('tagline_long'),
        ], 'Taglines'),

        MultiFieldPanel([
            FieldPanel('standard_donation_request'),
            FieldPanel('standard_mailinglist_request'),
        ], 'Default CTAs'),
    ]

    @property
    def donate_block(self):
        return {
            'heading': 'Support our work',
            'content': self.standard_donation_request,
            'target': self.donation_page,
        }

    @property
    def mailing_list_block(self):
        return {
            'heading': 'Sign up to our newsletter',
            'content': self.standard_mailinglist_request,
        }


def pre_save_image_or_doc(sender, instance, *args, **kwargs):
    if instance.file is not None:
        if instance.file.name.startswith('import_'):
            instance.import_ref = instance.file.name


models.signals.pre_save.connect(pre_save_image_or_doc, sender=StopwatchImage)
models.signals.pre_save.connect(
    pre_save_image_or_doc, sender=StopWatchDocument)
