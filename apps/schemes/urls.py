from django.urls import path
from . import views

app_name = 'schemes'

urlpatterns = [
    path('', views.scheme_list_view, name='list'),
    path('eligibility/', views.scheme_eligibility_view, name='eligibility'),
    path('<int:scheme_id>/', views.scheme_detail_view, name='detail'),
    path('<int:scheme_id>/bookmark/', views.scheme_bookmark_toggle, name='bookmark'),
]
