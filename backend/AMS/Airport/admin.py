from django.contrib import admin

from Airport.models import Mio_auth_user

# Register your models here.
class Mio_admin(admin.ModelAdmin):
    model=Mio_auth_user
    list_display=('username','password','role')
    

admin.site.register(Mio_auth_user,Mio_admin)