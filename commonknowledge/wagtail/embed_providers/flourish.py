import re
from html.parser import HTMLParser

from wagtail.embeds.finders.base import EmbedFinder
import requests


class FlourishFinder(EmbedFinder):
    FLOURISH_URL_PATTERN = re.compile(
        r'https://public.flourish.studio/visualisation/(\d+)/?')

    def accept(self, url):
        """
        Returns True if this finder knows how to fetch an embed for the URL.

        This should not have any side effects (no requests to external servers)
        """
        return self.FLOURISH_URL_PATTERN.match(url) is not None

    def find_embed(self, url, max_width=None):
        """
        Takes a URL and max width and returns a dictionary of information about the
        content to be used for embedding it on the site.

        This is the part that may make requests to external APIs.
        """
        match = self.FLOURISH_URL_PATTERN.match(url)
        if match is None:
            return None

        slug = match.group(1)

        return {
            'title': "Title of the content",
            'author_name': "StopWatch",
            'provider_name': "Flourish",
            'type': "rich",
            'width': max_width,
            'height': None,
            'thumbnail_url': _ThumbnailExtract.from_page_url(url),
            'html': f'<div class="flourish-embed flourish-table" data-src="visualisation/{slug}"></div>',
        }


class _ThumbnailExtract(HTMLParser):
    image = None

    @staticmethod
    def from_page_url(url):
        parser = _ThumbnailExtract()
        parser.feed(requests.get(url).text)

        return parser.image

    def handle_starttag(self, tag, attrs):
        if tag == 'meta' and self.get_attr(attrs, 'property') == 'og:image':
            self.image = self.get_attr(attrs, 'content')

    def get_attr(self, attrs, key):
        return next((val for attrkey, val in attrs if key == attrkey), None)
