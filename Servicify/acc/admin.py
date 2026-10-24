from django.contrib import admin
from django.contrib.auth.hashers import identify_hasher, make_password

from .models import Location, Service, User, Serviceman, Booking


class HashPasswordAdmin(admin.ModelAdmin):
    """If an admin types a plain password, hash it before saving."""

    def save_model(self, request, obj, form, change):
        try:
            identify_hasher(obj.password)       # already hashed -> fine
        except ValueError:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(HashPasswordAdmin):
    list_display = ('username', 'email', 'phone', 'location')
    list_filter = ('location',)
    search_fields = ('username', 'email', 'phone')


@admin.register(Serviceman)
class ServicemanAdmin(HashPasswordAdmin):
    list_display = ('username', 'service', 'location', 'phone', 'experience')
    list_filter = ('service', 'location')
    search_fields = ('username', 'email', 'phone')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'serviceman', 'booking_date', 'status')
    list_filter = ('status',)
