import json
from urllib import parse

from django import template
from django.conf import settings
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from commonknowledge.helpers import safe_to_int

from webpack_loader.templatetags import webpack_loader
register = template.Library()


@register.simple_tag
def webpack_bundle(name, type='js'):
    if settings.DEBUG:
        if type == 'js':
            return mark_safe(f'<script src="http://localhost:8080/{name}.js"></script>')
        else:
            return mark_safe('')

    else:
        return webpack_loader.render_bundle(name, type)


@register.simple_tag(takes_context=True)
def infinite_scroll_container(context, item_selector='iscroll_item', page=None, **kwargs):
    request: HttpRequest = context.get('request')

    params = request.GET.dict()
    params['page'] = '{{#}}'
    params['empty'] = '1'
    next_path_template = request.path + '?' + \
        parse.urlencode(params).replace('%7B%7B%23%7D%7D', '{{#}}')

    config = {
        'path': next_path_template,
        'append': item_selector,
        'history': False,
    }
    return mark_safe(f'data-infinite-scroll=\'{json.dumps(config)}\'')


@register.simple_tag(takes_context=True)
def filter_toggle_link(context, label, name, value, active_class='active', **kwargs):
    request: HttpRequest = context.get('request')
    params = request.GET.dict()

    classnames = [kwargs['class']] if 'class' in kwargs else []

    active = request.GET.get(name, None) == value
    if active:
        classnames.append(active_class)

    if len(classnames) > 0:
        classtag = format_html(' class="{}"', ' '.join(classnames))
    else:
        classtag = ''

    if params.get(name) == value:
        params.pop(name)
    else:
        params[name] = value

    if len(params) > 0:
        href = request.path + '?' + parse.urlencode(params)
    else:
        href = request.path

    return format_html(
        '<a href="{}"{}>{}</a>',
        href,
        classtag,
        label
    )
