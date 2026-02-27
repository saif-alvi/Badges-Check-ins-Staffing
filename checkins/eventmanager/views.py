from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
# Create your views here.

def index(request):
    template = loader.get_template("eventmanager/index.html")
    return render(request, "eventmanager/index.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        host = request.POST.get('is_host')
        username = email
        if User.objects.filter(email=email).exists():
            user = authenticate(request, username = username, password = password)
            if user is not None:
                auth_login(request,user)

                if host  == 'Y':
                    return redirect('host_eventpage')
                else:
                    return redirect('event_search')
            else:
                messages.error(request, "Email or Password is Incorrect")
                return render(request, 'eventmanager/login.html')
        else:
            messages.error(request, "User does not exist")
            return render(request, 'eventmanager/login.html')
    return render(request, 'eventmanager/login.html')
        

def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'eventmanager/signup.html')     
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'eventmanager/signup.html')

        user = User.objects.create_user(username = email, email = email, password=password)
        user.save()
        messages.success(request,"Account Created!")
        return redirect('login')
    return render(request, 'eventmanager/signup.html')


def event_search(request):
    return HttpResponse("Welcome to the event management platform!")

def event_signup_form(request):
    return HttpResponse("Welcome to the event management platform!")

def event_confirmation(request):
    return HttpResponse("Welcome to the event management platform!")

def host_eventpage(request):
    return HttpResponse("Welcome to the event management platform!")