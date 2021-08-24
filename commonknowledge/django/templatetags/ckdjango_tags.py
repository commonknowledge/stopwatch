import json
from urllib import parse

from django import template
from django.conf import settings
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join
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


@register.simple_tag
def filter_toggles(field, all_label='All', label_class="btn", **kwargs):
    classname = kwargs.pop('class', "btn-check")

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

    return format_html(
        '<select name="{}" {} aria-label="{}">{}</select>',
        field.name,
        mark_safe(f'class="{classname}"') if classname else '',
        field.label,
        choices_html
    )


@register.inclusion_tag('commonknowledge/django/bind_forms.html')
def bind_filter_form(**kwargs):
    return kwargs


def _href_with_qs(context, params=None):
    if params is None:
        query = {}
        params = context
    else:
        request: HttpRequest = context.get('request')
        query = request.GET.dict()

    query.update(params)
    return _qs_suffix(query)


def _qs_suffix(query):
    if len(query) > 0:
        return '?' + parse.urlencode(query)
    else:
        return ''
