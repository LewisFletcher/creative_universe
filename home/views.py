from django.views.generic.base import View, TemplateView
from django.shortcuts import render
from artpage.models import ArtPiece, Collection

 
class HomeView(View):
    def get(self, request):
        recent_art = ArtPiece.objects.order_by('-uploaded')[:3]
        collections = Collection.objects.order_by('-last_updated')[:3]
        context = {'recent_art' : recent_art, 'collections' : collections}
        return render(request, 'homepage.html', context)