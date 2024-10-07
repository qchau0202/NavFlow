from django.http import HttpResponse
from django.urls import include, path
def index(request):
    return HttpResponse("This is the homepage.")

urlpatterns = [
    path('', index),  
    path('polls/', include('polls.urls')),
    
]
