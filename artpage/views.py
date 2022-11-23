from django.shortcuts import render
from django.views.generic.base import View, TemplateView
# Create your views here.

class ArtView(View):
    def get(self, request):
        return render(request, 'artpage/arthome.html')