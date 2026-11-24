from django.urls import path
from . import views

app_name = 'wellness'

urlpatterns = [
    path('', views.wellness_home_view, name='home'),
    path('screen/', views.wellness_screen_view, name='screen'),
    path('catalog/', views.wellness_catalog_view, name='catalog'),
    path('<int:analysis_id>/', views.wellness_detail_view, name='detail'),
    path('<int:analysis_id>/pdf/', views.wellness_export_pdf, name='export_pdf'),
]
