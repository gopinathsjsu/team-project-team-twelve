from django.contrib import admin
from jwtapp.models import Mio_flight_schedule
from jwtapp.models import Mio_airline
from jwtapp.models import Mio_terminal
from jwtapp.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


# admin panel ka user interface mofication wala class:

class UserModelAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email', 'first_name','last_name','terms_conditions','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        #individual fields me ja ke dekhna...waha dikhega
        ('User credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','terms_conditions')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','terms_conditions','roles','airline_code','password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserModelAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.

class Mio_airlineAdmin(admin.ModelAdmin):
    list_display = ['airline_flight_key','airline_code','flight_code',]

admin.site.register(Mio_airline,Mio_airlineAdmin)


class Mio_terminalAdmin(admin.ModelAdmin):
    list_display=['terminal_gate']

admin.site.register(Mio_terminal,Mio_terminalAdmin)

class Mio_flight_schedule_Admin(admin.ModelAdmin):
    list_display=[field.name for field in Mio_flight_schedule._meta.get_fields()]

admin.site.register(Mio_flight_schedule,Mio_flight_schedule_Admin)