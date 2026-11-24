from django.urls import path
from . import public_views

app_name = 'public'

urlpatterns = [
    path('', public_views.home_view, name='home'),
    path('about/', public_views.about_view, name='about'),
    path('features/', public_views.features_view, name='features'),
    path('contact/', public_views.contact_view, name='contact'),
    path('faq/', public_views.faq_view, name='faq'),
    path('privacy/', public_views.privacy_view, name='privacy'),
    path('terms/', public_views.terms_view, name='terms'),
    path('web3-transparency/', public_views.web3_info_view, name='web3_info'),
]
