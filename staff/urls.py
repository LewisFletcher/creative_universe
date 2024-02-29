from . import views
from django.urls import path


urlpatterns = [
    path('custom-email/', views.CustomEmailView.as_view(), name='custom_email'),
    path('shipping-email/', views.ShippingEmailView.as_view(), name='shipping_email'),
]