from django.urls import path
from . import views

app_name = 'web3_ledger'

urlpatterns = [
    path('verify/', views.verify_receipt_view, name='verify'),
    path('receipt/<str:receipt_code>/', views.receipt_detail_view, name='receipt_detail'),
]
