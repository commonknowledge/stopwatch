
import re
from html.parser import HTMLParser
from urllib.parse import urlparse
from wagtail.embeds.finders.base import EmbedFinder
import requests
from django.utils.text import slugify


class ShinyFinder(EmbedFinder):
    SHINY_URL_PATTERN = re.compile(
        r'https://stop-watch.shinyapps.io/(.+)/?')

    def accept(self, url):
        """
        Returns True if this finder knows how to fetch an embed for the URL.
        This should not have any side effects (no requests to external servers)
        """
        return self.SHINY_URL_PATTERN.match(url) is not None

    def find_embed(self, url, max_width=None):
        """
        Takes a URL and max width and returns a dictionary of information about the
        content to be used for embedding it on the site.

        This is the part that may make requests to external APIs.
        """

        return {
            'title': "Title of the content",
            'author_name': "StopWatch",
            'provider_name': "Shiny",
            'type': "rich",
            'width': max_width,
            'height': None,
            'thumbnail_url': _ThumbnailExtract.from_page_url(url),
            'html': f'<iframe id="shiny-{slugify(url)}" src="{url}"></iframe>'
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
