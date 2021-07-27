from django.db import models
from wagtail.core.blocks import StructBlock, RichTextBlock, CharBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class ArticlesListBlock(StructBlock):
    heading = CharBlock()
    site_area = PageChooserBlock(required=False)


class CtaBlock(StructBlock):
    heading = CharBlock()
    image = ImageChooserBlock()
    content = RichTextBlock()
    target = PageChooserBlock()


class NewsletterSignupBlock(CtaBlock):
    pass
