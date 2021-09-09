from typing import NamedTuple
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.html import strip_tags

from commonknowledge.helpers import safe_to_int


class SortOption(NamedTuple):
    label: str
    slug: str
    ordering: strip_tags

    @staticmethod
    def to_field_choices(opts):
        return tuple(
            (opt.slug, opt.label)
            for opt in opts
        )


class ChildListMixin:
    allow_search = False
    sort_options = (
        SortOption('Newest', 'most_recent', '-first_published_at'),
        SortOption('Oldest', 'oldest', 'first_published_at'),
    )

    def get_sort(self, request):
        if len(self.sort_options) == 0:
            return None

        return next(
            (
                opt for opt in self.sort_options
                if opt.slug == request.GET.get('sort')
            ),
            self.sort_options[0]
        )

    def get_search_queryset(self, request, qs):
        q = request.GET.get('query')
        if q and self.allow_search:
            sort = self.get_sort(request)
            return qs.search(q, order_by_relevance=sort is None)

    def get_child_list_queryset(self, request):
        return self.get_children().live().specific()

    def get_page_size(self):
        return 20

    def get_filters(self, request):
        return None

    def get_filter_form(self, request):
        return None

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        qs = self.get_child_list_queryset(request)
        filter = self.get_filters(request)
        sort = self.get_sort(request)

        if filter:
            if isinstance(filter, dict):
                qs = qs.filter(**filter)
            else:
                qs = qs.filter(filter)

        if sort:
            qs = qs.order_by(sort.ordering)

        search = self.get_search_queryset(request, qs)
        if search is None:
            paginator = Paginator(qs, self.get_page_size())
        else:
            paginator = Paginator(search, self.get_page_size())

        page = safe_to_int(request.GET.get('page'), 1)

        if request.GET.get('empty') == '1':
            try:
                context['child_list_page'] = paginator.page(page)
            except PageNotAnInteger:
                context['child_list_page'] = paginator.page(1)
            except EmptyPage:
                context['child_list_page'] = None

            context['child_list_paginator'] = paginator
        else:
            context['child_list_page'] = paginator.get_page(page)

        context['filter_form'] = self.get_filter_form(request)

        return context
