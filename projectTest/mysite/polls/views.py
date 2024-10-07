from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def myapp(request):
    return ("Hello, world. You're at myapp index.")

def conmeo(request):
    return ("meomeow")