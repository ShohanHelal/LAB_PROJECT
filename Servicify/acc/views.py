
from django.shortcuts import render, redirect
from .forms import UserForm, ServicemanForm


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form})


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
    return render(request, 'login.html')

def serviceman_signin(request):
    return render(request, 'serviceman_signup.html')