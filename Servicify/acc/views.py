
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction

from .forms import UserForm, ServicemanForm
from .models import User, Serviceman, Booking


def register_choice(request):
    return render(request, 'register_choice.html')


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = UserForm()

    return render(request, 'SignUp.html', {'form': form})


def serviceman_signup(request):
    if request.method == 'POST':
        form = ServicemanForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = ServicemanForm()

    return render(
        request,
        'acc/serviceman_signup.html',
        {'form': form}
    )


def signin(request):
    error = ''

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', 'customer')

        if role == 'customer':
            account = User.objects.filter(
                username=username,
                password=password
            ).first()

            if account:
                request.session.flush()
                request.session['customer_id'] = account.id
                return redirect('booking')

        elif role == 'serviceman':
            account = Serviceman.objects.filter(
                username=username,
                password=password
            ).first()

            if account:
                request.session.flush()
                request.session['serviceman_id'] = account.id
                return redirect('serviceman_dashboard')

        error = 'Incorrect username, password, or account type.'

    return render(request, 'login.html', {'error': error})


def booking(request):
    customer_id = request.session.get('customer_id')

    if not customer_id:
        return redirect('signin')

    customer = User.objects.filter(id=customer_id).first()

    if not customer:
        request.session.flush()
        return redirect('signin')

    if request.method == 'POST':
        try:
            Booking.objects.create(
                service_name=request.POST.get(
                    'service_name', ''
                ).strip(),
                customer_name=request.POST.get(
                    'customer_name', ''
                ).strip(),
                phone=request.POST.get('phone', '').strip(),
                address=request.POST.get('address', '').strip(),
                booking_date=request.POST.get('booking_date'),
                booking_time=request.POST.get('booking_time'),
                offered_price=request.POST.get('offered_price') or 0
            )

            return render(request, 'booking.html', {
                'customer': customer,
                'success': 'Your booking has been submitted successfully!'
            })

        except (ValueError, TypeError):
            return render(request, 'booking.html', {
                'customer': customer,
                'error': (
                    'Please enter a valid date, time, '
                    'and offered price.'
                )
            })

    return render(request, 'booking.html', {'customer': customer})


def serviceman_dashboard(request):
    serviceman_id = request.session.get('serviceman_id')

    if not serviceman_id:
        return redirect('signin')

    provider = Serviceman.objects.filter(
        id=serviceman_id
    ).first()

    if not provider:
        request.session.flush()
        return redirect('signin')

    available_jobs = Booking.objects.filter(
        serviceman__isnull=True,
        status='Pending'
    ).order_by('booking_date', 'booking_time')

    my_jobs = Booking.objects.filter(
        serviceman=provider
    ).order_by('-created_at')

    earnings = sum(
        job.offered_price
        for job in my_jobs
        if job.status == 'Completed'
    )

    return render(request, 'serviceman_dashboard.html', {
        'provider': provider,
        'available_jobs': available_jobs,
        'my_jobs': my_jobs,
        'earnings': earnings
    })


@require_POST
def accept_job(request, booking_id):
    serviceman_id = request.session.get('serviceman_id')

    if not serviceman_id:
        return redirect('signin')

    provider = get_object_or_404(
        Serviceman,
        id=serviceman_id
    )

    
    # Assign the job only if it is still available.
    with transaction.atomic():
        accepted = Booking.objects.filter(
            id=booking_id,
            serviceman__isnull=True,
            status='Pending'
        ).update(
            serviceman=provider,
            status='Confirmed'
        )

    if accepted:
        request.session['job_message'] = (
            'Job accepted successfully.'
        )
    else:
        request.session['job_message'] = (
            'This job is no longer available.'
        )

    return redirect('serviceman_dashboard')
