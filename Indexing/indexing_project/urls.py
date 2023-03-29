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
from indexing_project import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    path('crawl/', views.crawl, name='crawl'),
    path('search/', views.search, name='search'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
]