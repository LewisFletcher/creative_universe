from django.shortcuts import render
from django.views.generic.base import View, TemplateView
from artpage.models import ArtPiece, Collection, ArtType
# Create your views here.

class ArtView(View):
    def get(self, request):
        art_type = ArtType.objects.all()
        art = ArtPiece.objects.order_by('-uploaded')
        collections = Collection.objects.all()
        context = {'arts' : art, 'collections' : collections, 'type' : art_type}
        return render(request, 'arthome.html', context)