from django.views.generic.base import View, TemplateView
from django.shortcuts import render


 
class HomeView(View):
    def get(self, request):
        return render(request, 'homepage.html')