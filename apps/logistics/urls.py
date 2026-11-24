from django.urls import path
from . import views

app_name = 'logistics'

urlpatterns = [
    path('', views.logistics_index_view, name='index'),
]
