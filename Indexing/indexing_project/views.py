from rest_framework import viewsets

from indexing_project.models import Products
from indexing_project.serializers import ProductsSerializer

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from indexing_project.documents import ProductsDocument
from django.shortcuts import render
from .forms import MyForm
from django.template import RequestContext
from elasticsearch_dsl.query import MoreLikeThis
from elasticsearch_dsl import Search
from math import ceil

def home(request):
    return render(request, 'home.html')


def search(request):
    q = request.GET.get('q')
    # rating_star= request.GET.get('rating_star')
    res = Q("multi_match", query=q, fields=["product_name"])
    if q:
        s = ProductsDocument.search().extra(size=100).query(res)
    
    f = Search()
    f = f.query(MoreLikeThis(like=q, fields=["product_name"]))
    f = f.source(exclude=["text"])
    response = f.execute()

    for hit in response:
        print(hit.product_name)
        print()

    form = MyForm(request.POST or None)
    if request.method == "POST":
        # Have Django validate the form for you
        if form.is_valid():
            # The "display_type" key is now guaranteed to exist and
            # guaranteed to be "displaybox" or "locationbox"
            rating = request.POST["rating"]
            location = request.POST["location"]
            print(rating)
            print(location)
            if rating == "4.5": 
                s = s.filter('range',rating={'gte':4.5,'lt':5.1})
            elif rating == "4" :
                s = s.filter('range',rating={'gte':4,'lt':4.5})
            else:
                s = s.filter('range',rating={'gte':0,'lt':4})

            if location == "local":
                s = s.filter('match',shop_location="Local")
            else:
                s = s.filter('match',shop_location="Overseas")
            

    return render(request, 'search.html', {'result': s.to_queryset(), 'query':q , 'form': form})

def round_to_multiple(number, multiple):
    return multiple * ceil(number / multiple)

def pie_chart(request):
    labels = []
    data = []
    labels1=[]
    data1=[]
    labels2=[]
    data2=[]
    extra=[]
    frequency = {}

    queryset = Products.objects.order_by('rating')
    count1=0
    count2=0
    count3=0
    count4=0
    count5=0
    count6=0

    for product in queryset:
        if product.rating >= 4:
            count1+=1
        elif product.rating >= 3:
            count2+=1
        elif product.rating >=2:
            count3+=1
        else:
            count4+=1

        if product.shop_location == "Local":
            count5+=1
        else:
            count6+=1

        num = round_to_multiple(product.product_price, 5)
        extra.append(num)

    labels.append("4 and above")
    data.append(count1)
    labels.append("3 to 3.99")
    data.append(count2)
    labels.append("2 to 2.99")
    data.append(count3)
    labels.append("Below 2")
    data.append(count4)

    labels1.append("Local")
    data1.append(count5)
    labels1.append("Overseas")
    data1.append(count6)

    for item in extra:
        # checking the element in dictionary
        if item in frequency:
            # incrementing the counr
            frequency[item] += 1
        else:
            # initializing the count
            frequency[item] = 1

    frequency = dict(sorted(frequency.items()))

    for key in frequency:
        labels2.append("$"+str(key))
        data2.append(frequency[key])

    return render(request, 'pie_chart.html', {
        'labels': labels,
        'data': data,
        'labels1': labels1,
        "data1": data1,
        'labels2': labels2,
        "data2": data2,
    })