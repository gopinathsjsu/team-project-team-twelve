from email.policy import default
from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name,last_name,roles,tc,password=None,password2=None):
        """
        Creates and saves a User with the given email,tc,name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            roles=roles,
            tc=tc
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name,roles,tc, password=None):
        """
        Creates and saves a superuser with the given email,name,tc,password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            roles=roles,
            tc=tc
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Mio_airline(models.Model):
    airline_flight_key=models.CharField(max_length=100,primary_key=True,blank=True)
    airline_code = models.CharField(max_length = 50)
    flight_code = models.CharField(max_length = 50)
    airline_name = models.CharField(max_length = 50)
    is_available = models.BooleanField(default=False)

    class Meta:
        unique_together = [['airline_code', 'flight_code']]

    def save(self, *args, **kwargs):
        self.airline_flight_key=self.airline_code+"_"+self.flight_code
        super(Mio_airline,self).save(*args, **kwargs)

    def __str__(self):
        return self.airline_name+"_"+self.airline_code+"_"+self.flight_code

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # date_of_birth = models.DateField()
    ROLES = (

        ('airport_employee', 'airport_employee'),
        ('airline_employee', 'airline_employee'),
        # ('customer', 'customer'),
        ('admin','admin')
    )
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    tc=models.BooleanField()
    roles = models.CharField(max_length=50, choices=ROLES, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    airline_code = models.ForeignKey(Mio_airline,on_delete = models.CASCADE,null=True,blank=True,related_name="airline")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','roles','tc']

    def __str__(self):  
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin





class Mio_terminal(models.Model):
    terminal = models.CharField(max_length = 50)
    gate = models.CharField(max_length = 50)
    gate_status = models.CharField(max_length = 50, default = 'open') #open, occupied, under_maintenance
    class Meta:
        unique_together = [['terminal', 'gate']]

from smart_selects.db_fields import ChainedForeignKey

class Mio_flight_schedule(models.Model):
    fact_guid = models.CharField(max_length=64, primary_key=True)
    airline_flight_key = models.ForeignKey(Mio_airline, related_name = 'flight_key',  on_delete = models.CASCADE)    
    source = models.CharField(max_length = 100)
    destination = models.CharField(max_length = 100)
    arrival_departure = models.CharField(max_length=12)
    time =  models.DateTimeField()
    terminal_code = models.ForeignKey(Mio_terminal, related_name = 'airport_terminal', null = True, on_delete = models.SET_NULL)
    gate_code = models.ForeignKey(Mio_terminal, related_name = 'terminal_gate', null = True, on_delete = models.SET_NULL)
    baggage_carousel = models.CharField(max_length = 100)
    remarks = models.CharField(max_length = 100)



