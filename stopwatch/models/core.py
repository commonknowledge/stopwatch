from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField, EmailField, TextField
from wagtail.core.blocks.field_block import CharBlock, PageChooserBlock, URLBlock
from wagtail.core.blocks.struct_block import StructBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.documents.models import Document, AbstractDocument
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel, FieldPanel
from wagtail.images.edit_handlers import FieldPanel
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
        FieldPanel('photo'),
        FieldPanel('bio'),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('twitter'),
            FieldPanel('website'),
        ], 'Contact Details')
    ]

    def __str__(self):
        return self.name


@register_snippet
class Organisation(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField(null=True)
    website = models.URLField(null=True)
    website_text = models.CharField(max_length=1024)

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('website'),
        FieldPanel('website_text')
    ]

    def __str__(self):
        return self.name


@register_setting
class SiteSettings(BaseSetting):
    class BottomLink(StructBlock):
        page = PageChooserBlock()
        label = CharBlock(required=False)

    bottom_page_links = StreamField(
        [('link', BottomLink())], blank=True, min_num=0, max_num=4)

    donate_page = models.ForeignKey(
        Page, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    email_list_url = models.URLField(blank=True, null=True)

    standard_donation_request = RichTextField(
        default='We aim to address excess and disproportionate stop and search, promote best practice and ensure fair, effective policing for all.')
    standard_mailinglist_request = RichTextField(
        default='Regular updates on our activities, noteworthy articles, and how you can get involved in our work.')

    tagline = RichTextField(
        default="",
        help_text='Text displayed at the base of a site')
    tagline_long = RichTextField(
        default="<strong>StopWatch</strong> is a coalition of legal experts, academics, citizens and civil liberties campaigners. We aim to address excess and disproportionate stop and search, promote best practice and ensure fair, effective policing for all.",
        help_text='Text displayed at the base of pages')

    address = CharField(
        default="2 Langley Lane London SW8 1GB", max_length=128)
    phone_number = CharField(default="+44 (0)208 226 5737", max_length=64)
    email_contact = EmailField(default="info@stop-watch.org")
    end_matter = TextField(default='Registered Charity No: 1161908')

    google_analytics_ua = TextField(verbose_name="Google Analytics UA",
                                    null=True, blank=True, help_text="Google Analytics UA, to allow setting up Google Analytics")

    panels = [
        MultiFieldPanel([
            FieldPanel('tagline'),
            FieldPanel('tagline_long'),
        ], 'Taglines'),

        MultiFieldPanel([
            FieldPanel('standard_donation_request'),
            FieldPanel('standard_mailinglist_request'),
            PageChooserPanel('donate_page'),
            FieldPanel('email_list_url'),
        ], 'Default CTAs'),

        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('phone_number'),
            FieldPanel('email_contact'),
            FieldPanel('end_matter'),
        ], 'Organisation info'),

        MultiFieldPanel([
            FieldPanel('google_analytics_ua'),
        ], 'Analytics'),

        FieldPanel('bottom_page_links'),
    ]

    @property
    def donate_block(self):
        return {
            'heading': 'Support our work',
            'content': self.standard_donation_request,
            'target': self.donate_page,
        }

    @property
    def mailing_list_block(self):
        return {
            'heading': 'Sign up to our newsletter',
            'content': self.standard_mailinglist_request,
            'target': {
                "title": "Subscribe",
                "url": self.email_list_url,
            }
        }


def pre_save_image_or_doc(sender, instance, *args, **kwargs):
    if instance.file is not None:
        if instance.file.name.startswith('import_'):
            instance.import_ref = instance.file.name


models.signals.pre_save.connect(pre_save_image_or_doc, sender=StopwatchImage)
models.signals.pre_save.connect(
    pre_save_image_or_doc, sender=StopWatchDocument)
