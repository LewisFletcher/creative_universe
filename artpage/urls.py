from django.urls import path
from . import views

urlpatterns = [
    path('art/', views.ArtView.as_view(), name='art'),
]