from django.shortcuts import render
from django.views.generic.base import View, TemplateView
# Create your views here.

class ShopView(View):
    def get(self, request):
        return render(request, 'shop/shop.html')