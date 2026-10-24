from django.urls import path
from . import views

urlpatterns = [
    # accounts
    path('register/', views.register_choice, name='register_choice'),
    path('signup/', views.signup, name='signup'),
    path('serviceman-signup/', views.serviceman_signup, name='serviceman_signup'),
    path('login/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),

    # customer: find a service -> providers -> profile -> book
    path('services/', views.service_list, name='service_list'),
    path('providers/', views.provider_list, name='provider_list'),
    path('provider/<int:serviceman_id>/', views.provider_profile, name='provider_profile'),
    path('book/<int:serviceman_id>/', views.book_service, name='book_service'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),

    # service provider: receive work
    path('dashboard/', views.serviceman_dashboard, name='serviceman_dashboard'),
    path('booking/<int:booking_id>/accept/', views.accept_booking, name='accept_booking'),
    path('booking/<int:booking_id>/decline/', views.decline_booking, name='decline_booking'),
    path('booking/<int:booking_id>/complete/', views.complete_booking, name='complete_booking'),
]
