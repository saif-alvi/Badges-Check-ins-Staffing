from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name ="index"),
    path("login/",views.login,name="login"),
    path("signup/",views.signup,name="signup"),
    path("event_search/",views.event_search,name="event_search"),
    path("event_signup_form/",views.event_signup_form,name="event_signup_form"),
    path("event_confirmation/",views.event_confirmation,name="event_confirmation"),
    path("host_eventpage/",views.host_eventpage,name="host_eventpage"),
]