from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("contact/", ContactCreateView.as_view(), name="contact"),
    path("projects/", ProjectListView.as_view(), name="projects"),
    path("<slug:slug>/", ProjectDetailView.as_view(), name="detail"),
]
