from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Event
# Create your views here.

def index(request):
    all_events = Event.objects.all()
    return render(request, 'eventmanager/index.html', {'events': all_events})

def login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = email
        if User.objects.filter(email=email).exists():
            user = authenticate(request, username = username, password = password)
            if user is not None:
                auth_login(request,user)
                return redirect('host_eventpage')

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



def event_signup_form(request):
    event = Event.objects.get(id=event_id)
    return render(request, 'eventmanager/event_signup_form.html', {'event': event})

def event_confirmation(request):
    return HttpResponse("Welcome to the event management platform!")

@login_required(login_url='login')
def host_eventpage(request):
    if request.method == "POST":
        Event.objects.create(
            host = request.user,
            event_name=request.POST.get('event_name'),
            event_date=request.POST.get('event_date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            event_type=request.POST.get('event_type'),
            venue_address=request.POST.get('venue_address'),
            event_desc=request.POST.get('event_desc'),
            event_capacity=request.POST.get('event_capacity', 0)
        )
        messages.success(request, 'Event Created!')
        return redirect('host_eventpage')
    user_events = Event.objects.filter(host=request.user)
    return render(request, 'eventmanager/host_eventpage.html', {'events': user_events})

@login_required(login_url='login')
def delete_event(request, event_id):
    if request.method == "POST":
        Event.objects.filter(id=event_id, host=request.user).delete()
        messages.success(request, 'Event Deleted!')
    return redirect('host_eventpage')

def logout(request):
    auth_logout(request)
    return redirect('index')

