from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.urls import reverse
from .models import FAQ
# Create your views here.

class FAQView(TemplateView):
    template_name = 'faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = FAQ.objects.all().order_by('order')
        return context