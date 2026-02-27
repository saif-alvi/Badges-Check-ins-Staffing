from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name ="index"),
    path("login/",views.login,name="login"),
    path("logout/",views.logout,name="logout"),
    path("signup/",views.signup,name="signup"),
    path("event_signup_form/<int:event_id>",views.event_signup_form,name="event_signup_form"),
    path("event_confirmation/",views.event_confirmation,name="event_confirmation"),
    path("host_eventpage/",views.host_eventpage,name="host_eventpage"),
    path("event_delete/<int:event_id>/", views.delete_event, name="event_delete"),
]