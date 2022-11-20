from email.policy import default
from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name,last_name,roles,terms_conditions,airline_code,password=None,password2=None):
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
            terms_conditions=terms_conditions,
            airline_code=airline_code
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name,roles,terms_conditions, password=None):
        """
        Creates and saves a superuser with the given email,name,tc,password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            roles=roles,
            terms_conditions=terms_conditions,
            airline_code=None
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Mio_airline_main(models.Model):
    airline_key = models.CharField(max_length=100,primary_key=True)
    def __str__(self):
        return self.airline_key


class Mio_airline(models.Model):
    airline_flight_key=models.CharField(max_length=100,primary_key=True,blank=True)
    airline_code = models.ForeignKey(Mio_airline_main, on_delete= models.CASCADE)
    flight_code = models.CharField(max_length = 50)
    airline_name = models.CharField(max_length = 50)
    is_available = models.BooleanField(default=False)

    class Meta:
        unique_together = [['airline_code', 'flight_code']]

    def __str__(self):
        return self.airline_flight_key

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
    terms_conditions=models.BooleanField()
    roles = models.CharField(max_length=50, choices=ROLES, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    airline_code = models.ForeignKey(Mio_airline_main, on_delete = models.CASCADE,null=True,blank=True,related_name="airline")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','roles','terms_conditions']

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
    terminal_gate = models.CharField(primary_key = True, max_length = 50)
    gate_status = models.CharField(max_length = 50, default = 'open') #open, occupied, under_maintenance
    
    def __str__(self):
        return self.terminal_gate
    

class Mio_flight_schedule(models.Model):
    fact_guid = models.CharField(max_length=64, primary_key=True)
    airline_flight_key = models.ForeignKey(Mio_airline, related_name = 'airline_flight',  on_delete = models.CASCADE)    
    source = models.CharField(max_length = 100)
    destination = models.CharField(max_length = 100)
    arrival_departure = models.CharField(max_length=12)
    time =  models.DateTimeField()
    terminal_gate_key = models.ForeignKey(Mio_terminal, related_name = 'airport_terminal_gate', null = True, blank = True, on_delete =  models.CASCADE)
    baggage_carousel = models.CharField(max_length = 100)
    remarks = models.CharField(max_length = 100)



