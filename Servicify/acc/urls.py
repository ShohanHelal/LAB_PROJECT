
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('serviceman-signup/', views.serviceman_signup, name='serviceman_signup'),
    path('login/', views.signin, name='signin'),
]
