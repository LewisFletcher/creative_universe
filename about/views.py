from django.shortcuts import render
from django.views.generic import View
from .models import Katelyn
from markdownx.utils import markdownify
from bs4 import BeautifulSoup
# Create your views here.

class AboutPage(View):
    def get(self, request):
        info = Katelyn.objects.get(id=1)
        html_content = markdownify(info.info)
        soup = BeautifulSoup(html_content, 'html.parser')
        heading_class_large = "text-2xl font-bold my-4"
        for h in soup.find_all(['h1']):
            h['class'] = h.get('class', []) + heading_class_large.split()
        heading_class_medium = "text-xl font-semibold my-4"
        for h in soup.find_all(['h2']):
            h['class'] = h.get('class', []) + heading_class_medium.split()
        heading_class_small = "text-lg my-4"
        for h in soup.find_all(['h3']):
            h['class'] = h.get('class', []) + heading_class_small.split()
        heading_class_smaller = "text-base my-4"
        for h in soup.find_all(['h4, h5, h6']):
            h['class'] = h.get('class', []) + heading_class_smaller.split()
        list_class = "list-disc list-inside my-4"
        for l in soup.find_all(['ul']):
            l['class'] = l.get('class', []) + list_class.split()
        list_class = "list-decimal list-inside my-4"
        for l in soup.find_all(['ol']):
            l['class'] = l.get('class', []) + list_class.split()
        paragraph_class = "my-4"
        for p in soup.find_all(['p']):
            p['class'] = p.get('class', []) + paragraph_class.split()
        image_class = "my-4"
        for i in soup.find_all(['img']):
            i['class'] = i.get('class', []) + image_class.split()
        link_class = "text-blue-500 hover:text-blue-700 visited:text-purple-600 my-4"
        for a in soup.find_all(['a']):
            a['class'] = a.get('class', []) + link_class.split()
        image_class = "max-w-[12rem] h-auto pr-4 pb-4"
        for i in soup.find_all(['img']):
            i['class'] = i.get('class', []) + image_class.split()
        for img in soup.find_all('img'):
            img['class'] = img.get('class', []) + ['markdownimg']


        info_converted = str(soup)
        context = {'info' : info_converted }
        return render(request, 'about.html', context)
