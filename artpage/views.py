from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView
from artpage.models import ArtPiece, Collection, ArtType
from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin
from django.http import JsonResponse
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
    paginate_by = 12

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
    
def get_art(request, pk):
    art = ArtPiece.objects.filter(pk=pk)
    data = {
        'image_url': art.image.url
    }
    return JsonResponse(data)

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

class CategoryView(DetailView, MultipleObjectMixin):
    paginate_by = 9
    model = ArtType
    template_name = 'type_view.html'
    def get_context_data(self, **kwargs):
        art_types = ArtType.objects.all()
        object_list = ArtPiece.objects.filter(art_type = self.get_object())       
        context = super(CategoryView, self).get_context_data(object_list=object_list,**kwargs, art_type=art_types)   
        return context