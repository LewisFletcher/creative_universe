"""creativeuniverse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import os
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings
from shop.views import payment_webhook


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('kateupdate/', admin.site.urls),
    path('', include('home.urls')),
    path('shop/', include('shop.urls')),
    path('portfolio/', include('artpage.urls')),
    path('about/', include('about.urls')),
    path('contact/', include('contact.urls')),
    path('staff/', include('staff.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('webhooks/stripe/', payment_webhook, name='stripe-webhook'),
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls')),
                    path("__reload__/", include("django_browser_reload.urls")),
                    ]
                    

urlpatterns += [
    path('favicon.ico', serve, {
            'path': 'favicon.ico',
            'document_root': os.path.join(BASE_DIR, 'staticfiles/favicon_io'),
        }
    ),
]
