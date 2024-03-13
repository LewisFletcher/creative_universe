from . import views
from django.urls import path


urlpatterns = [
    path('custom-email/', views.CustomEmailView.as_view(), name='custom_email'),
    path('shipping-email/', views.ShippingEmailView.as_view(), name='shipping_email'),
    path('view-orders/', views.ViewOrdersView.as_view(), name='view_orders'),
    path('order-detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order-complete/<int:pk>/', views.order_complete, name='order_complete'),
]