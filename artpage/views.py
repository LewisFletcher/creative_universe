from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView
from artpage.models import ArtPiece, Collection, ArtType
from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin
from django.http import JsonResponse
from django.urls import reverse
# Create your views here.


class ArtView(View):
    def get(self, request):
        art_type = ArtType.objects.all()
        art = ArtPiece.objects.all().order_by('-uploaded')[:9]
        collections = Collection.all_collections.order_by('-last_updated')[:9]
        context = {'arts' : art, 'collections' : collections, 'type' : art_type}
        return render(request, 'arthome.html', context)

class AllArtView(ListView):
    model = ArtPiece
    template_name = 'all_art.html'
    context_object_name = 'arts'
    paginate_by = 9

    def get_queryset(self):
        return ArtPiece.objects.order_by('-uploaded')
    
    def get_template_names(self):
        if self.request.htmx:
            return "art_loop.html"
        return "all_art.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['art_type'] = ArtType.objects.all()
        context["url"] = self.request.path
        return context

class AllCollectionView(ListView):
    model = Collection
    template_name = 'all_collections.html'
    context_object_name = 'collections'
    paginate_by = 9

    def get_queryset(self):
        return Collection.all_collections.order_by('-last_updated')
    
    def get_template_names(self):
        if self.request.htmx:
            return "collection_loop.html"
        return "all_collections.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['art_type'] = ArtType.objects.all()
        context["url"] = self.request.path
        return context

class ArtDetailView(DetailView):
    model = ArtPiece
    template_name = 'art_detail.html'
    context_object_name = 'art'

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'collection_detail.html'
    context_object_name = 'collection'

class CategoryView(DetailView, MultipleObjectMixin):
    paginate_by = 9
    model = ArtType
    template_name = 'type_view.html'
    def get_context_data(self, **kwargs):
        art_types = ArtType.objects.all()
        object_list = ArtPiece.objects.filter(art_type = self.get_object())       
        context = super(CategoryView, self).get_context_data(object_list=object_list,**kwargs, art_type=art_types)   
        return context