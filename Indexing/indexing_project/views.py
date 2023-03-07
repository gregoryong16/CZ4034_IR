# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.generic import TemplateView, ListView
# from django.db.models import Q
# from .models import Products
# from haystack.query import SearchQuerySet
# from haystack.generic_views import SearchView
# from haystack.forms import SearchForm
# from haystack.inputs import AutoQuery, Exact, Clean
# def home(request):
#     return render(request, 'home.html')

# # Create your views here.
# class NewSearchView(SearchView):
#     template_name = 'search\search.html'
#     form_class = SearchForm
#     queryset = SearchQuerySet()

#     def get_queryset(self):  # new
#         object_list = super(NewSearchView, self).get_queryset()
#         return object_list
    
# # class SearchResultsView(ListView):
# #     model = Products
# #     template_name = 'search\search.html'

# #     def get_queryset(self):  # new
# #         query = self.request.GET.get("q")
# #         object_list = Products.objects.filter(
# #             Q(name__icontains=query) 
# #         )
# #         return object_list
# # from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
# # from haystack.forms import FacetedSearchForm

# # # Now create your own that subclasses the base view
# # class FacetedSearchView(BaseFacetedSearchView):
# #     template_name = 'search\search.html'
# #     facet_fields = ['rating_star']
# #     form_class = FacetedSearchForm


from rest_framework import viewsets

from indexing_project.models import Products
from indexing_project.serializers import ProductsSerializer

# class ProductsViewSet(viewsets.ModelViewSet):
#     serializer_class = ProductsSerializer
#     queryset = Products.objects.all()

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from indexing_project.documents import ProductsDocument
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def search(request):
    q = request.GET.get('q')
    rating_star= request.GET.get('rating_star')
    res = Q("multi_match", query=q, fields=["name"])
    if q:
        s = ProductsDocument.search().extra(size=100).query(res).filter('match',rating_star = rating_star)

    else:
        result = ''

    return render(request, 'search.html', {'result': s.to_queryset(), 'query':q})

# class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
#     serializer_class = None
#     document_class = None

#     @abc.abstractmethod
#     def generate_q_expression(self, query):
#         """This method should be overridden
#         and return a Q() expression."""

#     def get(self, request, query):
#         try:
#             q = self.generate_q_expression(query)
#             search = self.document_class.search().query(q)
#             response = search.execute()

#             print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

#             results = self.paginate_queryset(response, request, view=self)
#             serializer = self.serializer_class(results, many=True)
#             return self.get_paginated_response(serializer.data)
#         except Exception as e:
#             return HttpResponse(e, status=500)


# # views
# class SearchProducts(PaginatedElasticSearchAPIView):
#     serializer_class = ProductsSerializer
#     document_class = ProductsDocument

#     def generate_q_expression(self, query):
#          return Q(
#                 'multi_match', query=query,
#                 fields=[
#                     'name'
#                 ], fuzziness='auto')

# For faceted search
# from elasticsearch_dsl import FacetedSearch, HistogramFacet, TermsFacet

# class ProductsSearch(FacetedSearch):
#     doc_types = [Products ]
#     # fields that should be searched
#     fields = ['name']

#     facets = {
#         # use bucket aggregations to define facets
#         # 'tags': TermsFacet(field='tags'),
#         # 'publishing_frequency': DateHistogramFacet(field='published_from', interval='month')
#         'rating_star' : HistogramFacet(field='rating_star',interval=1)
#     }

#     def search(self):
#         # override methods to add custom pieces
#         s = super().search()
#         return s.filter('match',rating_star = "4")

# from django.core.paginator import (
#     Paginator, Page, EmptyPage, PageNotAnInteger
# )

# def search2(request):
#     q = request.GET.get('q')
#     bs = ProductsSearch(q)
#     response = bs.execute()
#     paginator = Paginator(response, 100)
#     page = request.GET.get('page')
#     products = paginator.get_page(page)
#     return render(request, 'search.html', {'result': products})