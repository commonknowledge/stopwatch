
import re
from html.parser import HTMLParser
from urllib.parse import urlparse
from wagtail.embeds.finders.base import EmbedFinder
import requests
from django.utils.text import slugify


class ShinyFinder(EmbedFinder):
    SHINY_URL_PATTERN = re.compile(
        r'https://([\w\d-]+).shinyapps.io/([\w\d-]+)/*')

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
        url_parts = self.SHINY_URL_PATTERN.match(url)
        org_slug = url_parts.group(1)
        app_slug = url_parts.group(2)
        embed_id = f'shiny-{slugify(url)}'

        return {
            'title': f"Shiny app: {org_slug}/{app_slug}",
            'author_name': org_slug,
            'provider_name': "Shiny",
            'type': "rich",
            'width': max_width,
            'height': None,
            'thumbnail_url': "https://shiny.rstudio.com/images/shinySiteBandOne.png",
            'html': f'<iframe id="{embed_id}" src="{url}"></iframe>'
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
