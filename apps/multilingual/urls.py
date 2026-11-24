from django.urls import path
from . import views

app_name = 'multilingual'

urlpatterns = [
    path('switch/<str:lang_code>/', views.switch_language, name='switch'),
]
