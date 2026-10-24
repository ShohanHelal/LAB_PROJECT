from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db.models import Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from reviews.models import Review
from .decorators import customer_required, serviceman_required
from .forms import UserForm, ServicemanForm, BookingForm
from .models import User, Serviceman, Booking, Service, Location


def register_choice(request):
    return render(request, 'register_choice.html')


def signup(request):
    """Customer sign up."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! Please log in.')
            return redirect('signin')
    else:
        form = UserForm()
    return render(request, 'SignUp.html', {'form': form})


def serviceman_signup(request):
    """Service provider sign up."""
    if request.method == 'POST':
        form = ServicemanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Provider account created! Please log in.')
            return redirect('signin')
    else:
        form = ServicemanForm()
    return render(request, 'serviceman_signup.html', {'form': form})


def signin(request):
    error = ''
    next_url = request.POST.get('next') or request.GET.get('next') or ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'customer')

        if role == 'customer':
            account = User.objects.filter(username=username).first()
            if account and check_password(password, account.password):
                request.session.flush()
                request.session['customer_id'] = account.id
                safe = url_has_allowed_host_and_scheme(
                    next_url, allowed_hosts={request.get_host()}
                )
                return redirect(next_url if next_url and safe else 'service_list')

        elif role == 'serviceman':
            account = Serviceman.objects.filter(username=username).first()
            if account and check_password(password, account.password):
                request.session.flush()
                request.session['serviceman_id'] = account.id
                return redirect('serviceman_dashboard')

        error = 'Incorrect username, password, or account type.'

    return render(request, 'login.html', {'error': error, 'next': next_url})


def signout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('home')




def service_list(request):
    """Step 1: what service do you need?"""
    services = Service.objects.annotate(provider_count=Count('servicemen'))
    return render(request, 'service_list.html', {'services': services})


def provider_list(request):
    """Step 2: providers around your location.
    Filters come from the URL:  ?service=3&location=5
    """
    customer = User.objects.filter(
        id=request.session.get('customer_id')
    ).first()

    service_id = request.GET.get('service', '')
    location_id = request.GET.get('location')      # None = not in the URL
    using_my_area = False


    if location_id is None:
        if customer:
            location_id = str(customer.location_id)
            using_my_area = True
        else:
            location_id = ''

    providers = Serviceman.objects.select_related('service', 'location')
    if service_id.isdigit():
        providers = providers.filter(service_id=service_id)
    if location_id.isdigit():
        providers = providers.filter(location_id=location_id)

    # Best rated first
    providers = providers.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews'),
    ).order_by('-avg_rating', '-review_count', 'username')

    context = {
        'providers': providers,
        'services': Service.objects.all(),
        'locations': Location.objects.all(),
        'selected_service': service_id,
        'selected_location': location_id,
        'using_my_area': using_my_area,
    }
    return render(request, 'provider_list.html', context)


def provider_profile(request, serviceman_id):
    """Step 3: visit the provider's profile (public page)."""
    provider = get_object_or_404(
        Serviceman.objects.select_related('service', 'location'),
        id=serviceman_id
    )
    reviews = provider.reviews.select_related('customer')
    return render(request, 'provider_profile.html', {
        'provider': provider,
        'reviews': reviews,
        'average': provider.average_rating(),
        'done_jobs': provider.bookings.filter(status='Completed').count(),
    })


@customer_required
def book_service(request, customer, serviceman_id):
    """Step 4: book the provider."""
    provider = get_object_or_404(
        Serviceman.objects.select_related('service', 'location'),
        id=serviceman_id
    )

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = customer
            booking.serviceman = provider
            booking.save()
            messages.success(
                request,
                'Booking request sent! You will see the provider\'s contact '
                'details here once he accepts.'
            )
            return redirect('my_bookings')
    else:
        form = BookingForm(initial={'address': customer.address})

    return render(request, 'book_service.html', {
        'form': form, 'provider': provider
    })


@customer_required
def my_bookings(request, customer):
    bookings = customer.bookings.select_related(
        'serviceman', 'serviceman__service', 'serviceman__location', 'review'
    )
    return render(request, 'my_bookings.html', {
        'customer': customer, 'bookings': bookings
    })


@customer_required
@require_POST
def cancel_booking(request, customer, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=customer)
    if booking.status in ('Pending', 'Accepted'):
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled.')
    else:
        messages.error(request, 'This booking can no longer be cancelled.')
    return redirect('my_bookings')




@serviceman_required
def serviceman_dashboard(request, provider):
    bookings = provider.bookings.select_related(
        'customer', 'customer__location', 'review'
    )
    return render(request, 'serviceman_dashboard.html', {
        'provider': provider,
        'pending': bookings.filter(status='Pending'),
        'accepted': bookings.filter(status='Accepted'),
        'history': bookings.filter(
            status__in=['Completed', 'Declined', 'Cancelled']
        ),
        'completed_count': bookings.filter(status='Completed').count(),
        'average': provider.average_rating(),
        'latest_reviews': Review.objects.filter(
            serviceman=provider
        ).select_related('customer')[:5],
    })


@serviceman_required
@require_POST
def accept_booking(request, provider, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, serviceman=provider)
    if booking.status == 'Pending':
        booking.status = 'Accepted'
        booking.save()
        messages.success(
            request,
            'Job accepted. The customer\'s phone and email are now visible - '
            'contact him to agree on the price.'
        )
    else:
        messages.error(request, 'This request is no longer pending.')
    return redirect('serviceman_dashboard')


@serviceman_required
@require_POST
def decline_booking(request, provider, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, serviceman=provider)
    if booking.status == 'Pending':
        booking.status = 'Declined'
        booking.save()
        messages.success(request, 'Request declined.')
    else:
        messages.error(request, 'This request is no longer pending.')
    return redirect('serviceman_dashboard')


@require_POST
def complete_booking(request, booking_id):
    """Either the customer or the provider can mark an accepted job as done."""
    booking = get_object_or_404(Booking, id=booking_id)

    is_customer = request.session.get('customer_id') == booking.customer_id
    is_provider = request.session.get('serviceman_id') == booking.serviceman_id

    if not (is_customer or is_provider):
        messages.error(request, 'You are not allowed to do that.')
        return redirect('signin')

    if booking.status == 'Accepted':
        booking.status = 'Completed'
        booking.save()
        messages.success(request, 'Job marked as completed.')
    else:
        messages.error(request, 'Only an accepted job can be completed.')

    return redirect('serviceman_dashboard' if is_provider else 'my_bookings')

