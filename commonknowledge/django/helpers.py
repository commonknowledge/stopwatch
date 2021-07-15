from django.utils.html import format_html_join


def concat_html(*items):
    return format_html_join('', '{}', ((x,) for x in items))