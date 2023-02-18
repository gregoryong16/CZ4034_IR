from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

def home(request):
    return render(request, 'home.html')

# Create your views here.
