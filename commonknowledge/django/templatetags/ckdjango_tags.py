import json
from urllib import parse
from math import ceil

from django import template
from django.conf import settings
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join
from commonknowledge.helpers import safe_to_int

from webpack_loader.templatetags import webpack_loader
register = template.Library()


@register.simple_tag(takes_context=True)
def infinite_scroll_container(context, item_selector='.iscroll_item', page=None, **kwargs):
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

    json_config = json.dumps(config)

    return format_html('data-infinite-scroll="{}"', json_config)

@register.simple_tag
def filter_toggles(field, all_label='All', label_class="btn", **kwargs):
    classname = kwargs.pop('class', "btn-check")

    if not hasattr(field, 'field') or not hasattr(field, 'name'):
        return ''

    opts = format_html_join(
        '',
        '<input type="radio" class="{}" name="{}" value="{}" id="{}-{}" autocomplete="off" {}>' +
        '<label class="{}" for="{}-{}">{}</label>',
        (
            (
                classname,
                field.name,
                value,
                field.name,
                value,
                'checked' if field.value() == value else '',
                label_class,
                field.name,
                value,
                label
            )
            for value, label
            in field.field.choices
        ),
    )

    return format_html(
        '<input type="radio" class="{}" name="{}" value="{}" id="{}-{}" autocomplete="off" {}>' +
        '<label class="{}" for="{}-{}">{}</label>{}',
        classname,
        field.name,
        '',
        field.name,
        'all',
        'checked' if field.value() == '' else '',
        label_class,
        field.name,
        'all',
        all_label,
        opts
    )

@register.simple_tag
def filter_menu(field, **kwargs):
    classname = kwargs.pop('class', 'form-select')

    choices_html = format_html_join(
        '',
        '<option value="{}" {}>{}</option>',
        (
            (
                value,
                mark_safe('selected') if field.value() == value else '',
                label
            )
            for value, label
            in field.field.choices
        ),
    )

    id_html = format_html('id="{}"', kwargs['id']) if 'id' in kwargs else ''

    return format_html(
        '<select {} name="{}" {} aria-label="{}">{}</select>',
        id_html,
        field.name,
        format_html('class="{}"', classname) if classname else '',
        field.label,
        choices_html
    )

@register.inclusion_tag('commonknowledge/django/bind_forms.html')
def bind_filter_form(**kwargs):
    return kwargs


@register.filter
def splitgroup(value, arg):
    count, i = map(int, arg.split(','))
    group_size = ceil(len(value) / count)

    if i == count - 1:
        return value[group_size * i:]
    else:
        return value[group_size * i:group_size * (i + 1)]


def _qs_suffix(query):
    if len(query) > 0:
        return '?' + parse.urlencode(query)
    else:
        return ''
