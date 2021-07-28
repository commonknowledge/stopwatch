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


@register.inclusion_tag('ckwagtail/include/avatar.html')
def avatar(**kwargs):
    if 'name' in kwargs:
        name = kwargs['name'].split(' ')
        kwargs['initials'] = name[0][0].upper() + name[-1][0].upper()
    return kwargs
