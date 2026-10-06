from django.db import models

# Create your models here.
class User_acc(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    division = models.CharField(max_length=100, blank=True)
    police_station = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.user_name

class Ser_acc(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=100, blank=True)
    division = models.CharField(max_length=100, blank=True)
    police_station = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return f"{self.user_name} - {self.service}"

