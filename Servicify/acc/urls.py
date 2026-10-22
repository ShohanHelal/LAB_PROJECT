
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('serviceman-signup/', views.serviceman_signup,
         name='serviceman_signup'),
    path('register/', views.register_choice, name='register_choice'),
    path('login/', views.signin, name='signin'),
    path('booking/', views.booking, name='booking'),
    path('serviceman-dashboard/', views.serviceman_dashboard,
         name='serviceman_dashboard'),
    path('accept-job/<int:booking_id>/', views.accept_job,
         name='accept_job'),
]
