from django.urls import path
from . import views

urlpatterns = [
    path('contact', views.contact_us_view, name='contact')
]