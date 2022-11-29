from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView
from artpage.models import ArtPiece, Collection, ArtType
from django.core.paginator import Paginator
# Create your views here.


class ArtView(View):
    def get(self, request):
        art_type = ArtType.objects.all()
        art = ArtPiece.no_collection.order_by('-uploaded')[:9]
        collections = Collection.all_collections.order_by('-last_updated')[:9]
        context = {'arts' : art, 'collections' : collections, 'type' : art_type}
        return render(request, 'arthome.html', context)

class AllArtView(ListView):
    model = ArtPiece
    def get(self, request):
        art_type = ArtType.objects.all()
        arts = ArtPiece.objects.order_by('-uploaded')
        paginator = Paginator(arts, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        template = 'all_art.html'
        context = {
            'arts' : arts,
            'art_type' : art_type,
            'page_obj' : page_obj,
        }
        return render(request, template, context)

class AllCollectionView(ListView):
    model = Collection
    def get(self, request):
        art_type = ArtType.objects.all()
        collections= Collection.all_collections.order_by('-last_updated')
        paginator = Paginator(collections, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        template = 'all_collections.html'
        context = {
            'collections' : collections,
            'art_type' : art_type,
            'page_obj' : page_obj,
        }
        return render(request, template, context)

class ArtDetailView(DetailView):
    model = ArtPiece
    template_name = 'art_detail.html'
    context_object_name = 'art'

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'collection_detail.html'
    context_object_name = 'collection'