from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode

from .models import User, Serviceman


def _login_redirect(request):

    return redirect(
        reverse('signin') + '?' + urlencode({'next': request.get_full_path()})
    )


def customer_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        customer = User.objects.filter(
            id=request.session.get('customer_id')
        ).first()
        if customer is None:
            messages.error(request, 'Please log in as a customer to continue.')
            return _login_redirect(request)
        return view(request, customer, *args, **kwargs)
    return wrapper


def serviceman_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        provider = Serviceman.objects.filter(
            id=request.session.get('serviceman_id')
        ).first()
        if provider is None:
            messages.error(request, 'Please log in as a service provider to continue.')
            return redirect('signin')
        return view(request, provider, *args, **kwargs)
    return wrapper
