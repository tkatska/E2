from django.contrib import admin
from django.urls import path

from .views import contactView, successView, displayEmailView

urlpatterns = [
    path('contact/', contactView, name='contact'),
    path('success/', successView, name='success'),
    path('emails/', displayEmailView, name='emails'),
]