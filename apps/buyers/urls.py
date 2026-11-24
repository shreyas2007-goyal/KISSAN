from django.urls import path
from . import views

app_name = 'buyers'

urlpatterns = [
    path('', views.buyer_list_view, name='list'),
    path('<int:buyer_id>/', views.buyer_detail_view, name='detail'),
    path('enquire/<int:requirement_id>/', views.create_enquiry_view, name='enquire'),
]
