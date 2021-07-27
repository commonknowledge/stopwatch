from comms.models import NewsItem
from django.db import models
from wagtail.core.blocks import StructBlock, RichTextBlock, CharBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from commonknowledge.wagtail.helpers import get_children_of_type


class ArticlesListBlock(StructBlock):
    class Meta:
        template = 'widgets/articles_list_block.html'

    heading = CharBlock()
    image = ImageChooserBlock(required=False)
    site_area = PageChooserBlock(page_type='home.ListPage')

    def get_context(self, value, *args, **kwargs):
        context = super().get_context(value, *args, **kwargs)

        context['qs'] = value['site_area'].featured_items

        return context


class CtaBlock(StructBlock):
    heading = CharBlock()
    image = ImageChooserBlock()
    content = RichTextBlock()
    target = PageChooserBlock()


class NewsletterSignupBlock(CtaBlock):
    pass
