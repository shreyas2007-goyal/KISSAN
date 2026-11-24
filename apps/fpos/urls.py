from django.urls import path
from . import views

app_name = 'fpo'

urlpatterns = [
    path('', views.fpo_list_view, name='list'),
    path('<int:fpo_id>/', views.fpo_detail_view, name='detail'),
    path('<int:fpo_id>/join/', views.join_fpo_view, name='join'),
]
