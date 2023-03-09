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
from .forms import MyForm
from django.template import RequestContext

def home(request):
    return render(request, 'home.html')


def search(request):
    q = request.GET.get('q')
    # rating_star= request.GET.get('rating_star')
    res = Q("multi_match", query=q, fields=["name"])
    if q:
        s = ProductsDocument.search().extra(size=100).query(res)

    form = MyForm(request.POST or None)
    if request.method == "POST":
        # Have Django validate the form for you
        if form.is_valid():
            # The "display_type" key is now guaranteed to exist and
            # guaranteed to be "displaybox" or "locationbox"
            num_star = request.POST["num_star"]
            location = request.POST["location"]
            s = s.filter('match', rating_star = num_star)
            print(num_star)
            print(location)

    return render(request, 'search.html', {'result': s.to_queryset(), 'query':q , 'form': form})

