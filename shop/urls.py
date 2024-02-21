from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopView.as_view(), name='shop'),
    path('add-to-cart/<str:model_name>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<str:model_name>/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('create-checkout-session/', views.create_stripe_checkout_session, name='create_stripe_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancelled, name='payment_cancelled'),
]