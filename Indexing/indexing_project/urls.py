# from django.urls import path
# from django.conf.urls import include
# from .views import home
# from haystack.forms import FacetedSearchForm
# # from haystack.generic_views import FacetedSearchView
# from indexing_project.views import NewSearchView

# urlpatterns = [
#     path("", home, name="home"),
#     # path("search/", include('haystack.urls')),
#     path(r'search/', NewSearchView.as_view(), name='haystack_search'),
# ]

from django.urls import path, include
from rest_framework import routers

from indexing_project.views import home
# ProductsViewSet, SearchProducts
from indexing_project import views
# router = routers.DefaultRouter()
# router.register(r'product', ProductsViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('search/', views.search, name='search'),
]