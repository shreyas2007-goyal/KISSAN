from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/farmer/', views.register_farmer_view, name='register_farmer'),
    path('register/buyer/', views.register_buyer_view, name='register_buyer'),
    path('profile/', views.profile_view, name='profile'),
]
