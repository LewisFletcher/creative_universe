from django.urls import path
from . import views

urlpatterns = [
    path('', views.AboutPage.as_view(), name='about'),
]