
from django.shortcuts import render, redirect
from .forms import UserForm, ServicemanForm
from .models import User, Booking


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

    return render(request, 'serviceman_signup.html', {'form': form})


def signin(request):
    error = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        customer = User.objects.filter(
            username=username,
            password=password
        ).first()

        if customer:
            request.session['customer_id'] = customer.id
            return redirect('booking')
        else:
            error = 'Incorrect username or password.'

    return render(request, 'login.html', {'error': error})


def booking(request):
    customer_id = request.session.get('customer_id')

    if not customer_id:
        return redirect('signin')

    customer = User.objects.filter(id=customer_id).first()

    if not customer:
        return redirect('signin')

    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')

        Booking.objects.create(
            service_name=service_name,
            customer_name=customer_name,
            phone=phone,
            address=address,
            booking_date=booking_date,
            booking_time=booking_time
        )

        return render(request, 'booking.html', {
            'customer': customer,
            'success': 'Your booking has been submitted successfully!'
        })

    return render(request, 'booking.html', {
        'customer': customer
    })
