from django.shortcuts import render
from django.views.generic import View
from .models import Katelyn
# Create your views here.

class AboutPage(View):
    def get(self, request):
        info = Katelyn.objects.get(id=1)
        context = {'info' : info }
        return render(request, 'about.html', context)
