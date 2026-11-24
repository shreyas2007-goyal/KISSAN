from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.calculate_view, name='calculate'),
    path('export-pdf/', views.export_pdf_report, name='export_pdf'),
]
