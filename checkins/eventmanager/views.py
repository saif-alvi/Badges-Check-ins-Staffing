from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def index(request):
    template = loader.get_template("eventmanager/index.html")
    return render(request, "eventmanager/index.html")

def login(request):
    return HttpResponse("Welcome to the event management platform!")

def signup(request):
    return HttpResponse("Welcome to the event management platform!")

def event_search(request):
    return HttpResponse("Welcome to the event management platform!")

def event_signup_form(request):
    return HttpResponse("Welcome to the event management platform!")

def event_confirmation(request):
    return HttpResponse("Welcome to the event management platform!")

def host_eventpage(request):
    return HttpResponse("Welcome to the event management platform!")