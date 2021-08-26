from django.utils.html import escape
from wagtail.core.rich_text import RichText


class ListableMixin:
    title: str
    url: str

    @ property
    def intro_text(self):
        if hasattr(self, 'description'):
            text = _get_first_text_block(self.description)
            if text:
                return text

        if hasattr(self, 'summary'):
            text = _get_first_text_block(self.summary)
            if text:
                return text


def _get_first_text_block(stream):
    if stream is None:
        return None

    if isinstance(stream, RichText):
        return stream

    if isinstance(stream, str):
        return RichText(stream)
