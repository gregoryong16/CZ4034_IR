from django.urls import path
from django.conf.urls import include
from .views import home
from haystack.forms import FacetedSearchForm
# from haystack.generic_views import FacetedSearchView
from indexing_project.views import FacetedSearchView

urlpatterns = [
    path("", home, name="home"),
    path("search/", include('haystack.urls')),
    path(r'search/', FacetedSearchView.as_view(), name='haystack_search'),
]
