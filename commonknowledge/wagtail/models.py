from typing import NamedTuple
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.html import strip_tags

from commonknowledge.helpers import safe_to_int
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.http import Http404
from taggit.models import Tag
from wagtail.core.models import Page


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

    def get_pagination_context(self, request):
        context = {}
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

        page = min(paginator.num_pages, max(
            1, safe_to_int(request.GET.get('page'), 1)))

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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(self.get_pagination_context(request))
        return context


class ExploreTagsMixin(RoutablePageMixin):
    can_explore_tags = True

    # will override the default Page serving mechanism
    @route(r'^tagged/(?P<tag_slug>.+)/$')
    def tagged_pages(self, request, tag_slug, *args, **kwargs):
        parent_page = self
        tag = Tag.objects.filter(slug=tag_slug).first()
        if tag is None:
            raise Http404(f'The "{tag_slug}" tag doesn\'t exist.')

        class PaginationContext(ChildListMixin):
            def get_child_list_queryset(self, request):
                from stopwatch.models.pages import Article
                qs = Article.objects.filter(tags=tag).descendant_of(
                    parent_page).live().public().all()
                return qs

            def get_filter_form(self, request):
                from stopwatch.forms import CategoryFilterForm
                return CategoryFilterForm(data=request.GET)

        return self.render(request, context_overrides={
            'display_mode': 'tag_explorer',
            'tag': tag,
            **PaginationContext().get_pagination_context(request)
        })
