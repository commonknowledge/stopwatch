from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from bs4 import BeautifulSoup
from django.core.exceptions import ImproperlyConfigured
from wagtail.embeds.finders.oembed import OEmbedFinder
from wagtail.embeds.oembed_providers import youtube


class YouTubeFinder(OEmbedFinder):
    """ OEmbed finder which fixes various issues with YouTube's oEmbed API

    See: https://wagtail.io/blog/fixing-youtubes-oembed-implementation-custom-finder-class/

    """

    def __init__(self, providers=None, options=None):
        if providers is None:
            providers = [youtube]

        if providers != [youtube]:
            raise ImproperlyConfigured(
                'The YouTubePreserveRelFinder only operates on the youtube provider'
            )

        super().__init__(providers=providers, options=options)

    def accept(self, url):
        return self._get_endpoint(url) is not None

    def find_embed(self, url, max_width=None):
        embed = super().find_embed(url, max_width)

        soup = BeautifulSoup(embed['html'], 'html.parser')
        iframe_url = soup.find('iframe').attrs['src']
        scheme, netloc, path, params, query, fragment = urlparse(
            iframe_url)
        querydict = parse_qs(query)
        querydict['rel'] = 'none'
        query = urlencode(querydict, doseq=1)

        iframe_url = urlunparse(
            (scheme, netloc, path, params, query, fragment))
        iframe = soup.find('iframe')

        iframe.attrs['src'] = iframe_url
        iframe['class'] = (iframe.attrs.get(
            'class', '') + ' youtube-embed').strip()

        embed['html'] = str(soup)

        return embed
