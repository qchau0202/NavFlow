from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', index),
    path("polls/", include("polls.urls")),
]