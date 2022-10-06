from django.contrib import admin

from Airport.models import Mio_user

# Register your models here.
class Mio_admin(admin.ModelAdmin):
    model=Mio_user
    list_display=('fact_guid','username','password','role','is_active')
    

admin.site.register(Mio_user,Mio_admin)