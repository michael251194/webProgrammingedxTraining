from django.shortcuts import render
#from urllib3 import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
#def index(request):
#    return HttpResponse("Hello, world")
def index(request):
    return render(request, "hello/index.html")

def brian(request):
    return HttpResponse("hello, Brian")

#def greet(request, name):
#    return HttpResponse(f"hello, {name.capitalize()}")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name" : name.capitalize()
    })