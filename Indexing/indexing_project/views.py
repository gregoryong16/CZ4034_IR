from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from .models import Products
def home(request):
    return render(request, 'home.html')

# Create your views here.
class SearchResultsView(ListView):
    model = Products
    template_name = 'search.html'

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Products.objects.filter(
            Q(name__icontains=query) 
        )
        return object_list

from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.forms import FacetedSearchForm
# Now create your own that subclasses the base view
class FacetedSearchView(BaseFacetedSearchView):
    form_class = FacetedSearchForm
    facet_fields = ['rating_star']
    template_name = 'search.html'
    context_object_name = 'page_object'