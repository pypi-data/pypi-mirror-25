from django.conf import settings


class BaseSearchBackend:
    search_template = 'search/search.html'
    quick_search_template = 'search/quick_search.html'

    def __init__(self, request):
        self.request = request

    def get_queryset(self, query_str, limit=None):
        pass

    def get_search_template(self):
        return self.search_template

    def get_quick_search_template(self):
        return self.quick_search_template

    def search_view(self):
        pass

    def quick_search_view(self):
        pass


class SimpleProductSearchBackend(BaseSearchBackend):
    PAGINATE_BY = getattr(settings, 'PCART_SEARCH_PAGINATE_BY', 20)

    def get_queryset(self, query_str, limit=None):
        from pcart_catalog.models import Product
        from django.db.models import Q
        products = Product.objects.filter(
            Q(translations__title__icontains=query_str) | Q(variants__translations__title__icontains=query_str),
            published=True,
            status__is_searchable=True,
        )
        products = products.prefetch_related('variants')
        products = products.prefetch_related('status')
        products = products.prefetch_related('images')
        products = products.prefetch_related('translations')
        products = products.prefetch_related('variants__translations')

        if limit is not None:
            products = products[:limit]
        return products

    def search_view(self):
        from django.shortcuts import render
        from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

        query_str = self.request.GET.get('query')
        page = int(self.request.GET.get('page', 1))

        if query_str:
            products = self.get_queryset(query_str)

            _products_list = products
            paginator = Paginator(_products_list, self.PAGINATE_BY)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)
        else:
            products = None

        context = {
            'query': query_str,
            'products': products,
            'page_number': page,
            'page_url': self.request.path,
        }
        return render(self.request, self.get_search_template(), context)
