from django.contrib import admin

# Register your models here.
from .models import Event #, Attendee

admin.site.register(Event)
#admin.site.register(Attendee)