
from django.contrib import admin
from .models import User, Serviceman
from .models import Booking


admin.site.register(User)
admin.site.register(Serviceman)
admin.site.register(Booking)
