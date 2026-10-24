from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Avg


phone_validator = RegexValidator(
    regex=r'^(\+?88)?01[3-9]\d{8}$',
    message='Enter a valid mobile number like 01712345678.'
)


class Location(models.Model):
    """An area inside Dhaka (Mirpur, Gulshan, Farmgate ...)."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    """A type of work (Plumbing, Electrical, AC Repair ...)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    # Name of a Font Awesome icon, for example "faucet" or "bolt"
    icon = models.CharField(max_length=50, default='screwdriver-wrench')
    # Optional picture shown on the home page
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class User(models.Model):
    """A customer who looks for and books services."""
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)          # stored hashed
    phone = models.CharField(max_length=15, validators=[phone_validator])
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name='customers'
    )
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Serviceman(models.Model):
    """A service provider. Each provider offers ONE service in ONE area."""
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)          # stored hashed
    phone = models.CharField(max_length=15, validators=[phone_validator])
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, related_name='servicemen'
    )
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name='servicemen'
    )
    address = models.CharField(max_length=255)
    experience = models.PositiveIntegerField(default=0)   # years
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

    def average_rating(self):
        """Average of all review ratings, or None if no reviews yet."""
        avg = self.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg, 1) if avg else None


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),      # customer sent the request
        ('Accepted', 'Accepted'),    # provider accepted
        ('Declined', 'Declined'),    # provider said no
        ('Cancelled', 'Cancelled'),  # customer cancelled
        ('Completed', 'Completed'),  # work finished
    ]

    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings'
    )
    serviceman = models.ForeignKey(
        Serviceman, on_delete=models.CASCADE, related_name='bookings'
    )
    description = models.TextField()      # what work is needed
    address = models.TextField()          # where the work will be done
    booking_date = models.DateField()
    booking_time = models.TimeField()
    offered_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.customer} -> {self.serviceman} ({self.status})'

    def contact_visible(self):
        """Phone / email are shared only after the provider accepts."""
        return self.status in ('Accepted', 'Completed')
