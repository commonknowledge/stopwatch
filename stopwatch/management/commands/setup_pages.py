from urllib.parse import urlparse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from wagtail.core.models import Page, Site
from django.core import management

from stopwatch.models.pages import Article, Category, LandingPage

# Basic config
root_page_model = LandingPage
DEFAULT_WAGTAIL_PAGE_TITLE = "Welcome to your new Wagtail site!"


class Command(BaseCommand):
    help = "Set up essential pages"

    def add_arguments(self, parser):
        default_base_url = urlparse(settings.WAGTAILADMIN_BASE_URL)

        parser.add_argument(
            "--scratch", dest="scratch", type=bool, default=False
        )
        parser.add_argument(
            "--ensure-site", dest="ensure-site", type=bool, default=False
        )
        parser.add_argument(
            "--ensure-pages", dest="ensure-pages", type=bool, default=False
        )
        parser.add_argument(
            "-H", "--host", dest="host", type=str, default=default_base_url.hostname
        )
        parser.add_argument(
            "-p", "--port", dest="port", type=int, default=default_base_url.port or 80
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options.get("scratch", False):
            self.wipe_wagtail_data()
        else:
            self.hide_wagtail_default_pages()

        if options.get("ensure-site", False):
            home, root = self.setup_root_pages(
                options.get("host"), options.get("port"))

            if options.get("ensure-pages", False):
                ensure_child_page = self.ensure_child_page_factory(home)
                self.ensure_initial_pages(ensure_child_page)

    def ensure_initial_pages(self, ensure_child_page):
        ensure_child_page(
            Article(slug="about-stopwatch", title="About Stopwatch"))
        ensure_child_page(Category(slug="vacancies", title="Vacancies"))
        ensure_child_page(
            Category(slug="news-and-opinion", title="News and Opinion"))
        ensure_child_page(
            Category(slug="t-and-c", title="Terms and Conditions"))
        ensure_child_page(
            Category(slug="t-and-c", title="Terms and Conditions"))
        ensure_child_page(Category(slug="vacancies", title="Vacancies"))
        ensure_child_page(Category(slug="what-we-do", title="What we do"))
        ensure_child_page(Category(slug="experiences", title="Experiences"))

    def setup_root_pages(self, host: str, port: int):
        try:
            site = Site.objects.get(
                root_page__content_type=ContentType.objects.get_for_model(
                    root_page_model)
            )
            home = site.root_page
            print("Site and homepage already set up", site, home)
        except:
            home = root_page_model(
                title=settings.WAGTAIL_SITE_NAME,
                slug=slugify(settings.WAGTAIL_SITE_NAME),
            )
            root = Page.get_first_root_node()
            if root is None:
                root = Page.add_root(title="Content Root", slug="root")

            root.add_child(instance=home)

            site = Site.objects.get_or_create(
                hostname=host,
                port=port,
                is_default_site=True,
                site_name=settings.WAGTAIL_SITE_NAME,
                root_page=home,
            )
        return home, root

    def hide_wagtail_default_pages(self):
        # Delete placeholders
        Page.objects.filter(title=DEFAULT_WAGTAIL_PAGE_TITLE).all().unpublish()

    def wipe_wagtail_data(self):
        Page.objects.all().delete()
        Site.objects.all().delete()
        management.call_command("fixtree")

    def ensure_child_page_factory(self, root_page: Page):
        def ensure_child_page(page_instance: Page, parent_page=root_page):
            existing = parent_page.get_children().filter(slug=page_instance.slug)
            if not existing.exists():
                parent_page.add_child(instance=page_instance)
            else:
                model = existing.first().specific_class
                if model != page_instance.specific_class:
                    raise ValueError(
                        f"Slug exists ({page_instance.slug}), but type {model} !== required type {page_instance.specific_class}. Manual intervention required."
                    )
                print("Already exists:",
                      f"Page created: \"{page_instance.title}\" id={page_instance.id} content_type={page_instance.specific_class._meta.app_label}.{page_instance.specific_class.__name__} path={page_instance.url_path}"
                      )
            return page_instance

        return ensure_child_page
