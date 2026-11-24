from django.urls import path
from . import views

app_name = 'markets'

urlpatterns = [
    path('', views.market_list_view, name='list'),
    path('compare/', views.market_compare_view, name='compare'),
    path('<int:mandi_id>/', views.market_detail_view, name='detail'),
]
