from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_dispatcher, name='dispatcher'),
    path('farmer/', views.farmer_dashboard, name='farmer_dashboard'),
    path('buyer/', views.buyer_dashboard, name='buyer_dashboard'),
    path('fpo/', views.fpo_dashboard, name='fpo_dashboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
]
