from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Event
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, Attendee
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer


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



def event_signup_form(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == "POST":
        email = request.POST.get('email')
        first = request.POST.get('first_name')
        last = request.POST.get('last_name')
        title = request.POST.get('title')
        staff =request.POST.get('staff')
        if staff == None:
            staff = False
        else:
            staff = True

        if Attendee.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'eventmanager/event_signup_form.html', {'event': event})
        else:

            subject = "You're confirmed for "+ event.event_name
            message = (
                "Hi " + first + ",\n\n"
                "You're confirmed for " + event.event_name + ".\n"
                "Date: " + event.event_date + "\n"
                "Time: " + event.start_time + " - " + event.end_time + "\n"
                "Location: " + event.venue_address + "\n\n"
                "Thanks for signing up!"
            )

            send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,[email],fail_silently=False)
            messages.success(request, 'Check your inbox for confirmation!')
            Attendee.objects.create(
                    event=event,
                    email=email,
                    first_name=first,
                    last_name=last,
                    title=title,
                    attending_as_staff=staff
                )
            return redirect('index')
   
    return render(request, 'eventmanager/event_signup_form.html', {'event': event})



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


@login_required(login_url='login')
def event_attendee_pdf(request, attendee_id):
    attendee = Attendee.objects.get(id=attendee_id, event__host=request.user)
    event = attendee.event

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + event.event_name + '_attendee_' + str(attendee.id) + '.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    title = Paragraph(event.event_name + " - Attendee Details", styles['Normal'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    attendee_info = Paragraph(
        "<b>Email:</b> " +attendee.email + "<br/>" +
        "<b>First Name:</b> "+attendee.first_name + "<br/>" +
        "<b>Last Name:</b> "+attendee.last_name + "<br/>" +
        "<b>Title:</b> "+attendee.title + "<br/>" +
        "<b>Staff:</b> " + ("Yes" if attendee.attending_as_staff else "No") + "<br/>" +
        "<b>Event Date:</b> " + event.event_date + "<br/>" +
        "<b>Event Time:</b> " + event.start_time + " - " + event.end_time + "<br/>" +
        "<b>Event Location:</b> " + event.venue_address,
        styles['Normal']
    )
    elements.append(attendee_info)

    doc.build(elements)

    return response

