from django.urls import path
from indexing_project import views

urlpatterns = [
    path("", views.home, name="home"),
]