from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Serviceman(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    service_name = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Booking(models.Model):

    service_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    booking_date = models.DateField()
    booking_time = models.TimeField()

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name + " - " + self.service_name
