from email.policy import default
from django.db import models

# Create your models here.

class Mio_auth_user(models.Model):
    username=models.EmailField(max_length=254, primary_key=True)
    password=models.CharField(max_length=100)
    role=models.CharField(max_length=64)

class Mio_airline(models.Model):
    airline_code = models.CharField(max_length = 50)
    flight_code = models.CharField(max_length = 50)
    airline_name = models.CharField(max_length = 50)
    is_available = models.BooleanField(default=False)
    class Meta:
        unique_together = [['airline_code', 'flight_code']]

class Mio_user(models.Model):
    username = models.OneToOneField(Mio_auth_user, primary_key=True, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    user_type = models.CharField(max_length = 50)
    airline_code = models.ForeignKey(Mio_airline, on_delete = models.CASCADE)


class Mio_terminal(models.Model):
    
    terminal = models.CharField(max_length = 50)
    gate = models.CharField(max_length = 50)
    gate_status = models.CharField(max_length = 50, default = 'open') #open, occupied, under_maintenance
    class Meta:
        unique_together = [['terminal', 'gate']]



class Mio_flight_schedule(models.Model):
    fact_guid = models.CharField(max_length=64, primary_key=True)
    flight = models.ForeignKey(Mio_airline, related_name = 'airline_flight',  on_delete = models.CASCADE)
    airline = models.ForeignKey(Mio_airline,  on_delete = models.CASCADE)
    source = models.CharField(max_length = 100)
    destination = models.CharField(max_length = 100)
    arrival_departure = models.CharField(max_length = 100)
    time =  models.DateTimeField()
    terminal_code = models.ForeignKey(Mio_terminal, related_name = 'airport_terminal', null = True, on_delete = models.SET_NULL)
    gate_code = models.ForeignKey(Mio_terminal, related_name = 'terminal_gate', null = True, on_delete = models.SET_NULL)
    baggage_carousel = models.CharField(max_length = 100)
    remarks = models.CharField(max_length = 100)



""" class Mio_baggage_carousel(models.Model):
    terminal = models.ForeignKey(Mio_terminal, on_delete = models.CASCADE)
    carousel = models.CharField(max_length = 50, primary_key=True)
    carousel_status = models.models.BooleanField(default=False, default = True)
    class Meta:
        unique_together(('terminal', 'carousel')) """