from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
# Create your views here.

def index(request):
    template = loader.get_template("eventmanager/index.html")
    return render(request, "eventmanager/index.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        host = request.POST.get('is_host')

        if not User.objects.filter(password = password).exists() or not User.objects.filter(email=email).exists():
            messages.error(request, 'Email or Password not correct')
            return render(request, 'eventmanager/login.html')
          
        if User.objects.filter(password = password).exists() and User.objects.filter(email=email).exists() and host == "Y":
            return redirect('host_eventpage')
        
        if User.objects.filter(password = password).exists() and User.objects.filter(email=email).exists() and host == "N":
            return redirect('event_search')



    return render(request, 'eventmanager/login.html')

def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('pass_confirm')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'eventmanager/signup.html')     
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'eventmanager/signup.html')

        user = User.objects.create_user(email = email, password=password)
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