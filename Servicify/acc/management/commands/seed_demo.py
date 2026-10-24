"""Creates sample customers, providers, bookings and reviews for testing.

Run:   python manage.py seed_demo
All demo accounts use the password:  demo1234
"""
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils import timezone

from acc.models import Location, Service, User, Serviceman, Booking
from reviews.models import Review

PASSWORD = 'demo1234'

CUSTOMERS = [
    # username, email, phone, area, address
    ('rahim', 'rahim@example.com', '01711000001', 'Mirpur', 'House 12, Road 3, Mirpur 10'),
    ('nadia', 'nadia@example.com', '01711000002', 'Gulshan', 'Flat 5B, Gulshan Avenue'),
]

PROVIDERS = [
    # username, email, phone, service, area, years, bio
    ('karim_plumber', 'karim@example.com', '01811000001', 'Plumbing', 'Mirpur', 8,
     'Fixing leaks, taps and bathroom fittings for 8 years.'),
    ('sohel_plumber', 'sohel@example.com', '01811000002', 'Plumbing', 'Mohammadpur', 5,
     'Fast and clean plumbing work.'),
    ('babul_electric', 'babul@example.com', '01811000003', 'Electrical', 'Farmgate', 10,
     'Licensed electrician. House wiring, fans, lights.'),
    ('jamal_electric', 'jamal@example.com', '01811000004', 'Electrical', 'Mirpur', 4,
     'Electrical repair and new connections.'),
    ('arif_ac', 'arif@example.com', '01811000005', 'AC Repair', 'Gulshan', 6,
     'AC servicing, gas refill, installation.'),
    ('mina_cleaner', 'mina@example.com', '01811000006', 'Home Cleaning', 'Mirpur', 3,
     'Deep cleaning for flats and offices.'),
    ('rubel_painter', 'rubel@example.com', '01811000007', 'Painting', 'Mohammadpur', 7,
     'Interior and exterior painting.'),
    ('hasan_driver', 'hasan@example.com', '01811000008', 'Driver', 'Gulshan', 12,
     'Experienced driver, knows all of Dhaka.'),
]

REVIEWS = [
    # provider, customer, rating, comment
    ('karim_plumber', 'rahim', 5, 'Fixed the leaking pipe in 30 minutes. Very polite.'),
    ('karim_plumber', 'nadia', 4, 'Good work, came on time.'),
    ('babul_electric', 'rahim', 5, 'Very skilled electrician.'),
    ('arif_ac', 'nadia', 4, 'AC works great now.'),
]


class Command(BaseCommand):
    help = 'Create demo customers, providers and reviews'

    def handle(self, *args, **options):
        password = make_password(PASSWORD)

        for username, email, phone, area, address in CUSTOMERS:
            User.objects.get_or_create(username=username, defaults={
                'email': email, 'phone': phone, 'address': address,
                'location': Location.objects.get(name=area), 'password': password,
            })

        for username, email, phone, service, area, years, bio in PROVIDERS:
            Serviceman.objects.get_or_create(username=username, defaults={
                'email': email, 'phone': phone, 'address': area + ', Dhaka',
                'service': Service.objects.get(name=service),
                'location': Location.objects.get(name=area),
                'experience': years, 'bio': bio, 'password': password,
            })

        for provider, customer, rating, comment in REVIEWS:
            provider = Serviceman.objects.get(username=provider)
            customer = User.objects.get(username=customer)
            if Review.objects.filter(serviceman=provider, customer=customer).exists():
                continue
            booking = Booking.objects.create(
                customer=customer, serviceman=provider,
                description='Demo job', address=customer.address,
                booking_date=timezone.localdate() - timedelta(days=3),
                booking_time='10:00', status='Completed',
            )
            Review.objects.create(
                booking=booking, customer=customer, serviceman=provider,
                rating=rating, comment=comment,
            )

        self.stdout.write(self.style.SUCCESS(
            'Demo data ready. Log in with password: ' + PASSWORD
        ))
