from django.shortcuts import render
from django.views.generic.base import View, TemplateView
# Create your views here.

class AboutPage(View):
    def get(self, request):
        return render(request, 'about.html')