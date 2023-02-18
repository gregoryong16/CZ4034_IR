from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("IR Project")

# Create your views here.
