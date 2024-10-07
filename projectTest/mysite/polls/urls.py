from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('myapp', views.myapp, name = 'myapp'), 
]
