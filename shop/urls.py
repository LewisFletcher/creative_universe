from django.urls import path
from . import views
from artpage.views import ItemDetailView

urlpatterns = [
    path('', views.ShopView.as_view(), name='shop'),
    path('add-to-cart/<str:model_name>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<str:model_name>/<int:item_id>/', views.update_cart, name='update_cart'),
    path('stickers/details/<int:pk>', ItemDetailView.as_view(), name='sticker_detail'),
    path('photography-prints/details/<int:pk>', ItemDetailView.as_view(), name='photography_detail'),
    path('prints/details/<int:pk>', ItemDetailView.as_view(), name='print_detail'),
    path('merch/details/<int:pk>', ItemDetailView.as_view(), name='merch_detail'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('create-checkout-session/', views.create_stripe_checkout_session, name='create_stripe_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancelled, name='payment_cancelled'),
]