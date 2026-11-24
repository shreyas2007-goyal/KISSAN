from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.dashboard.public_urls', namespace='public')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('markets/', include('apps.markets.urls', namespace='markets')),
    path('calculator/', include('apps.calculator.urls', namespace='calculator')),
    path('wellness/', include('apps.crop_wellness.urls', namespace='wellness')),
    path('schemes/', include('apps.schemes.urls', namespace='schemes')),
    path('assistant/', include('apps.assistant.urls', namespace='assistant')),
    path('accessibility/', include('apps.accessibility.urls', namespace='accessibility')),
    path('multilingual/', include('apps.multilingual.urls', namespace='multilingual')),
    path('buyers/', include('apps.buyers.urls', namespace='buyers')),
    path('fpo/', include('apps.fpos.urls', namespace='fpo')),
    path('logistics/', include('apps.logistics.urls', namespace='logistics')),
    path('web3/', include('apps.web3_ledger.urls', namespace='web3_ledger')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
