from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from commonknowledge.helpers import safe_to_int


class ChildListMixin:
    def get_child_list_queryset(self):
        return self.get_children().order_by('-first_published_at').specific()

    def get_page_size(self):
        return 20

    def get_filters(self, request):
        return None

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        qs = self.get_child_list_queryset()
        filter = self.get_filters(request)

        if filter:
            if isinstance(filter, dict):
                qs = qs.filter(**filter)
            else:
                qs = qs.filter(filter)

        paginator = Paginator(qs, self.get_page_size())
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

        return context
