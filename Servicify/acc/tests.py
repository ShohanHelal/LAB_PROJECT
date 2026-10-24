from datetime import timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from reviews.models import Review
from .models import Location, Service, User, Serviceman, Booking


# A fast password hasher keeps the tests quick (real site uses the default one)
@override_settings(PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'])
class ServicifyFlowTests(TestCase):
    """Run with:  python manage.py test"""

    @classmethod
    def setUpTestData(cls):
        # Locations and services come from the data migration
        cls.mirpur = Location.objects.get(name='Mirpur')
        cls.gulshan = Location.objects.get(name='Gulshan')
        cls.plumbing = Service.objects.get(name='Plumbing')

    def setUp(self):
        self.signup_customer('rahim', 'rahim@x.com', '01711111111', self.mirpur)
        self.signup_customer('nadia', 'nadia@x.com', '01722222222', self.gulshan)
        self.signup_provider('karim', 'karim@x.com', '01833333333', self.mirpur)
        self.signup_provider('sohel', 'sohel@x.com', '01844444444', self.gulshan)
        self.karim = Serviceman.objects.get(username='karim')
        self.sohel = Serviceman.objects.get(username='sohel')

    # ---------- helpers ----------
    def signup_customer(self, username, email, phone, location):
        return self.client.post(reverse('signup'), {
            'username': username, 'email': email, 'password': 'secret123',
            'phone': phone, 'location': location.id, 'address': 'Some road',
        })

    def signup_provider(self, username, email, phone, location):
        return self.client.post(reverse('serviceman_signup'), {
            'username': username, 'email': email, 'password': 'secret123',
            'phone': phone, 'service': self.plumbing.id, 'location': location.id,
            'address': 'Shop', 'experience': 5, 'bio': 'hello',
        })

    def login(self, username, role='customer'):
        self.client.logout()
        return self.client.post(reverse('signin'), {
            'username': username, 'password': 'secret123', 'role': role,
        })

    def book(self, provider, **extra):
        data = {
            'description': 'Fix my kitchen tap',
            'address': 'House 1, Mirpur',
            'booking_date': (timezone.localdate() + timedelta(days=2)).isoformat(),
            'booking_time': '10:30',
            'offered_price': '500',
        }
        data.update(extra)
        return self.client.post(reverse('book_service', args=[provider.id]), data)

    # ---------- basic pages ----------
    def test_public_pages_load(self):
        for name in ['home', 'service_list', 'provider_list', 'register_choice',
                     'signin', 'signup', 'serviceman_signup']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)
        r = self.client.get(reverse('provider_profile', args=[self.karim.id]))
        self.assertEqual(r.status_code, 200)

    def test_only_dhaka_locations_exist(self):
        names = set(Location.objects.values_list('name', flat=True))
        for n in ['Mirpur', 'Farmgate', 'Mohammadpur', 'Gulshan']:
            self.assertIn(n, names)

    # ---------- accounts ----------
    def test_passwords_are_hashed_and_login_works(self):
        self.assertNotEqual(User.objects.get(username='rahim').password, 'secret123')
        r = self.login('rahim')
        self.assertRedirects(r, reverse('service_list'))
        r = self.client.post(reverse('signin'), {
            'username': 'rahim', 'password': 'wrong', 'role': 'customer'})
        self.assertContains(r, 'Incorrect username')

    def test_customer_cannot_login_as_serviceman(self):
        r = self.client.post(reverse('signin'), {
            'username': 'rahim', 'password': 'secret123', 'role': 'serviceman'})
        self.assertContains(r, 'Incorrect username')

    def test_login_redirects_to_next(self):
        url = reverse('book_service', args=[self.karim.id])
        r = self.client.get(url)          # not logged in
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse('signin'), r.url)
        r = self.client.post(r.url, {
            'username': 'rahim', 'password': 'secret123', 'role': 'customer',
            'next': url})
        self.assertRedirects(r, url)

    def test_next_to_other_site_is_ignored(self):
        r = self.client.post(reverse('signin'), {
            'username': 'rahim', 'password': 'secret123', 'role': 'customer',
            'next': 'https://evil.example.com/'})
        self.assertRedirects(r, reverse('service_list'))

    def test_bad_phone_rejected(self):
        r = self.signup_customer('bob', 'bob@x.com', '123', self.mirpur)
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username='bob').exists())

    def test_logout(self):
        self.login('rahim')
        self.client.get(reverse('signout'))
        r = self.client.get(reverse('my_bookings'))
        self.assertEqual(r.status_code, 302)

    # ---------- find providers ----------
    def test_provider_filter_by_location_and_default_area(self):
        # anonymous: everyone
        r = self.client.get(reverse('provider_list'), {'service': self.plumbing.id})
        self.assertEqual(len(r.context['providers']), 2)
        # explicit location filter
        r = self.client.get(reverse('provider_list'),
                            {'service': self.plumbing.id, 'location': self.gulshan.id})
        self.assertEqual([p.username for p in r.context['providers']], ['sohel'])
        # logged-in customer from Mirpur sees Mirpur providers by default
        self.login('rahim')
        r = self.client.get(reverse('provider_list'), {'service': self.plumbing.id})
        self.assertEqual([p.username for p in r.context['providers']], ['karim'])
        # ...but can choose "all of Dhaka"
        r = self.client.get(reverse('provider_list'),
                            {'service': self.plumbing.id, 'location': ''})
        self.assertEqual(len(r.context['providers']), 2)

    def test_garbage_filters_do_not_crash(self):
        r = self.client.get(reverse('provider_list'), {'service': 'abc', 'location': 'x'})
        self.assertEqual(r.status_code, 200)

    # ---------- booking flow ----------
    def test_full_happy_path(self):
        # customer books
        self.login('rahim')
        r = self.book(self.karim)
        self.assertRedirects(r, reverse('my_bookings'))
        booking = Booking.objects.get()
        self.assertEqual(booking.status, 'Pending')

        # while pending the provider's contact is hidden from the customer
        r = self.client.get(reverse('my_bookings'))
        self.assertNotContains(r, '01833333333')
        self.assertNotContains(r, 'karim@x.com')

        # provider sees the request but not the customer's phone/email yet
        self.login('karim', 'serviceman')
        r = self.client.get(reverse('serviceman_dashboard'))
        self.assertContains(r, 'Fix my kitchen tap')
        self.assertNotContains(r, '01711111111')
        self.assertNotContains(r, 'rahim@x.com')

        # provider accepts -> now sees customer's contact
        r = self.client.post(reverse('accept_booking', args=[booking.id]))
        self.assertRedirects(r, reverse('serviceman_dashboard'))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Accepted')
        r = self.client.get(reverse('serviceman_dashboard'))
        self.assertContains(r, '01711111111')
        self.assertContains(r, 'rahim@x.com')

        # customer now sees the provider's contact
        self.login('rahim')
        r = self.client.get(reverse('my_bookings'))
        self.assertContains(r, '01833333333')
        self.assertContains(r, 'karim@x.com')

        # cannot review before completion
        r = self.client.get(reverse('add_review', args=[booking.id]))
        self.assertRedirects(r, reverse('my_bookings'))

        # job done
        self.client.post(reverse('complete_booking', args=[booking.id]))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Completed')

        # review
        r = self.client.post(reverse('add_review', args=[booking.id]),
                             {'rating': 4, 'comment': 'Nice work'})
        self.assertRedirects(r, reverse('provider_profile', args=[self.karim.id]))
        review = Review.objects.get()
        self.assertEqual(review.serviceman, self.karim)
        self.assertEqual(self.karim.average_rating(), 4.0)

        # appears on profile and home
        r = self.client.get(reverse('provider_profile', args=[self.karim.id]))
        self.assertContains(r, 'Nice work')
        self.assertContains(self.client.get(reverse('home')), 'Nice work')

        # second review for the same booking is blocked
        self.client.post(reverse('add_review', args=[booking.id]),
                         {'rating': 1, 'comment': 'again'})
        self.assertEqual(Review.objects.count(), 1)

    def test_provider_can_decline(self):
        self.login('rahim')
        self.book(self.karim)
        booking = Booking.objects.get()
        self.login('karim', 'serviceman')
        self.client.post(reverse('decline_booking', args=[booking.id]))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Declined')
        # cannot accept after declining
        self.client.post(reverse('accept_booking', args=[booking.id]))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Declined')

    def test_customer_can_cancel_pending_and_accepted(self):
        self.login('rahim')
        self.book(self.karim)
        b1 = Booking.objects.get()
        self.client.post(reverse('cancel_booking', args=[b1.id]))
        b1.refresh_from_db()
        self.assertEqual(b1.status, 'Cancelled')

        self.book(self.karim)
        b2 = Booking.objects.exclude(id=b1.id).get()
        self.login('karim', 'serviceman')
        self.client.post(reverse('accept_booking', args=[b2.id]))
        self.login('rahim')
        self.client.post(reverse('cancel_booking', args=[b2.id]))
        b2.refresh_from_db()
        self.assertEqual(b2.status, 'Cancelled')

    def test_cannot_touch_other_peoples_bookings(self):
        self.login('rahim')
        self.book(self.karim)
        booking = Booking.objects.get()

        # another customer cannot cancel it
        self.login('nadia')
        r = self.client.post(reverse('cancel_booking', args=[booking.id]))
        self.assertEqual(r.status_code, 404)

        # another provider cannot accept it
        self.login('sohel', 'serviceman')
        r = self.client.post(reverse('accept_booking', args=[booking.id]))
        self.assertEqual(r.status_code, 404)

        # and cannot mark it completed
        self.client.post(reverse('complete_booking', args=[booking.id]))
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Pending')

        # another customer cannot review it
        r = self.client.get(reverse('add_review', args=[booking.id]))
        self.assertEqual(r.status_code, 302)   # redirected to login (nadia is not logged as customer now)

    def test_provider_cannot_use_customer_pages_and_vice_versa(self):
        self.login('karim', 'serviceman')
        self.assertEqual(self.client.get(reverse('my_bookings')).status_code, 302)
        self.assertEqual(self.client.get(reverse('book_service', args=[self.sohel.id])).status_code, 302)
        self.login('rahim')
        self.assertEqual(self.client.get(reverse('serviceman_dashboard')).status_code, 302)

    def test_action_urls_need_post(self):
        self.login('rahim')
        self.book(self.karim)
        booking = Booking.objects.get()
        r = self.client.get(reverse('cancel_booking', args=[booking.id]))
        self.assertEqual(r.status_code, 405)

    def test_past_date_rejected(self):
        self.login('rahim')
        yesterday = (timezone.localdate() - timedelta(days=1)).isoformat()
        r = self.book(self.karim, booking_date=yesterday)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)

    def test_price_is_optional(self):
        self.login('rahim')
        r = self.book(self.karim, offered_price='')
        self.assertRedirects(r, reverse('my_bookings'))
        self.assertEqual(Booking.objects.get().offered_price, 0)
        self.assertContains(self.client.get(reverse('my_bookings')), 'negotiated')

    def test_provider_profile_never_shows_contact(self):
        r = self.client.get(reverse('provider_profile', args=[self.karim.id]))
        self.assertNotContains(r, '01833333333')
        self.assertNotContains(r, 'karim@x.com')
