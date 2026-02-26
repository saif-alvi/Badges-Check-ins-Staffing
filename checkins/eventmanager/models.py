from django.db import models

# Create your models here.
class Event(models.Model):
    host_name = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    event_date = models.CharField(max_length=200)
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
    event_type = models.CharField(max_length=200)
    venue_address = models.CharField(max_length=200)
    event_desc = models.CharField(max_length=200)
    attendee_count = models.IntegerField(default=0)
    attendee_checkedin = models.IntegerField(default=0)
    staff_count = models.IntegerField(default=0)
    staff_checkedin = models.IntegerField(default=0)
    event_capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.event_name

class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    attending_as_staff = models.BooleanField()

    def __str__(self):
        return self.email