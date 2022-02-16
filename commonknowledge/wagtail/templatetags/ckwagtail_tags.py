from django.template.exceptions import TemplateSyntaxError
from wagtail.core.models import Site
from django import template
from wagtail.core.rich_text import get_text_for_indexing
from django.utils.html import format_html, format_html_join

register = template.Library()


@register.inclusion_tag('ckwagtail/include/menubar.html', takes_context=True)
def menubar(context, **kwargs):
    site = Site.find_for_request(context.get('request'))
    if site is None:
        return

    root = site.root_page
    kwargs['pages'] = root.get_children().in_menu()
    kwargs['request'] = context.get('request')

    return kwargs


class MainMenuNode (template.Node):
    def __init__(self, nodelist, flat=False):
        self.nodelist = nodelist
        self.flat = flat
        self.max_depth = 2 if flat else 12

    def get_children(self, qs, depth):
        if depth >= self.max_depth:
            return ()

        children = tuple(
            self.build_tree(child, index, depth + 1)
            for index, child
            in enumerate(qs)
        )

        if self.flat:
            children = tuple(
                inner_child
                for child in children
                for inner_child in ((child,) + child['children']())
            )

        return children

    def build_tree(self, page, index=0, depth=0):
        qs = page.get_children().in_menu().specific()
        return {
            'index': index,
            'first': index == 0,
            'page': page,
            'routable': getattr(page, 'is_routable', True),
            'children': lambda: self.get_children(qs, depth),
            'leaf': not qs.exists(),
        }

    def render(self, context):
        site = Site.find_for_request(context.get('request'))
        tree = self.build_tree(site.root_page)

        if self.flat:
            context['menu'] = tree['children']
        else:
            context['menu'] = tree

        output = self.nodelist.render(context)
        return output


@register.tag
def mainmenu(parser, token):
    nodelist = parser.parse(('endmainmenu',))
    parser.delete_first_token()
    return MainMenuNode(nodelist)


@register.tag
def mainmenu_flat(parser, token):
    nodelist = parser.parse(('endmainmenu',))
    parser.delete_first_token()
    return MainMenuNode(nodelist, flat=True)


@register.inclusion_tag('ckwagtail/include/avatar.html')
def avatar_img(**kwargs):
    if 'name' in kwargs:
        name = kwargs['name'].split(' ')
        kwargs['initials'] = name[0][0].upper() + name[-1][0].upper()
    return kwargs


@register.simple_tag(takes_context=True)
def breadcrumbs(context, page, **kwargs):
    page = page.get_parent()
    classname = kwargs.pop('class', 'breadcrumb')
    item_classname = kwargs.pop('item_class', 'breadcrumb-item')
    crumbs = []

    while page and not page.is_site_root():
        crumbs.append(page)
        page = page.get_parent()

    inner_html = format_html_join(
        '',
        '<li class="{}"><a href="{}">{}</a></li>',
        (
            (item_classname, page.url, page.title)
            for page in crumbs
        )
    )

    return format_html('<ol class="{}">{}</ol>', classname, inner_html)


@register.filter
def plaintext(text):
    return get_text_for_indexing(str(text))
