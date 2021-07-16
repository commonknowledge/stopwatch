from django.core.paginator import Paginator

from commonknowledge.helpers import safe_to_int


class ChildListMixin:
    def get_child_list_queryset(self):
        return self.get_children()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        paginator = Paginator(self.get_child_list_queryset(), 20)
        page = safe_to_int(request.GET.get('page'), 1)
        context['child_list_page'] = paginator.get_page(page)
        context['child_list_paginator'] = paginator

        return context
