from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from acc.decorators import customer_required
from acc.models import Booking
from .forms import ReviewForm
from .models import Review


@customer_required
def add_review(request, customer, booking_id):

    booking = get_object_or_404(Booking, id=booking_id, customer=customer)


    if booking.status != 'Completed':
        messages.error(request, 'You can review a job only after it is completed.')
        return redirect('my_bookings')


    if Review.objects.filter(booking=booking).exists():
        messages.error(request, 'You have already reviewed this job.')
        return redirect('my_bookings')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.customer = customer
            review.serviceman = booking.serviceman
            review.save()
            messages.success(request, 'Thank you! Your review has been posted.')
            return redirect('provider_profile', serviceman_id=booking.serviceman.id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'booking': booking})
