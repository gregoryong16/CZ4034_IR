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