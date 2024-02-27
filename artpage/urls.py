from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArtView.as_view(), name='portfolio'),
    path('art/', views.AllArtView.as_view(), name='all_art'),
    path('art/details/<int:pk>', views.ItemDetailView.as_view(), name='art_detail'),
    path('collections/', views.AllCollectionView.as_view(), name='all_collections'),
    path('collections/details/<int:pk>', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('type/<int:pk>',views.CategoryView.as_view(), name='category'),
]