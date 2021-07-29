from django.template.exceptions import TemplateSyntaxError
from wagtail.core.models import Site
from django import template
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


@register.tag
def mainmenu(parser, token):
    class MainMenuNode (template.Node):
        def __init__(self, nodelist):
            self.nodelist = nodelist

        def build_tree(self, page, index=0, depth=0):
            qs = page.get_children().in_menu()
            return {
                'index': index,
                'first': index == 0,
                'page': page,
                'children': lambda: tuple(
                    self.build_tree(child, index, depth + 1)
                    for index, child
                    in enumerate(qs)
                ),
                'leaf': not qs.exists(),
            }

        def render(self, context):
            site = Site.find_for_request(context.get('request'))
            context['menu'] = self.build_tree(site.root_page)

            output = self.nodelist.render(context)
            return output

    nodelist = parser.parse(('endmainmenu',))
    parser.delete_first_token()
    return MainMenuNode(nodelist)


@register.inclusion_tag('ckwagtail/include/avatar.html')
def avatar(**kwargs):
    if 'name' in kwargs:
        name = kwargs['name'].split(' ')
        kwargs['initials'] = name[0][0].upper() + name[-1][0].upper()
    return kwargs
