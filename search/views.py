from commonknowledge.wagtail.search.views import BasicSearchView

class SearchView(BasicSearchView):
    template_name = 'search/basic.html'
