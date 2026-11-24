from django.urls import path
from . import views

app_name = 'accessibility'

urlpatterns = [
    path('toggle/', views.toggle_accessibility, name='toggle'),
]
