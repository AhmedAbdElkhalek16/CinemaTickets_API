from django.contrib import admin
from .models import Guest,Reservation,Movie,Post

# Register your models here.
# admin_username:- admin
#admin_password:- anaadmin123

admin.site.register(Guest)
admin.site.register(Reservation)
admin.site.register(Movie)
admin.site.register(Post)

