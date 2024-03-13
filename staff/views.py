from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView
from .forms import CustomEmailForm, ShippingEmailForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.models import Order, OrderProduct
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.urls import reverse

class CustomEmailView(TemplateView, LoginRequiredMixin):
    template_name = 'custom_email_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CustomEmailForm()
        return context
    
    def post(self, request):
        form = CustomEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            html_content = render_to_string('custom_email.html', {'message': message})
            plain_message = strip_tags(html_content)

            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_content,
                from_email="support@creativeuniverseproductions.com",
                recipient_list=[email],
                fail_silently=False,
            )

            return render(request, 'custom_email_form.html', {'form': form, 'success': True})
        return render(request, 'custom_email_form.html', {'form': form, 'success': False})

class ShippingEmailView(TemplateView, LoginRequiredMixin):
    template_name = 'custom_email_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ShippingEmailForm()
        return context
    
    def post(self, request):
        form = ShippingEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            tracking_number = form.cleaned_data.get('tracking_number')
            carrier = form.cleaned_data.get('carrier')

            html_content = render_to_string('shipping_email.html', {
                'message': message, 
                'tracking_number': tracking_number, 
                'carrier': carrier
            })
            plain_message = strip_tags(html_content)

            send_mail(
                subject=subject,
                message=plain_message,
                html_message=html_content,
                from_email="support@creativeuniverseproductions.com",
                recipient_list=[email],
                fail_silently=False,
            )

            return render(request, 'custom_email_form.html', {'form': form, 'success': True})
        return render(request, 'custom_email_form.html', {'form': form, 'success': False})
    
class ViewOrdersView(ListView, LoginRequiredMixin):
    template_name = 'view_orders.html'
    model = Order
    
    def get_queryset(self):
        return Order.objects.all().order_by('-order_date').exclude(completed=True)
    
class OrderDetailView(DetailView, LoginRequiredMixin):
    template_name = 'order_detail.html'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(id=self.kwargs['pk'])
        order_products = OrderProduct.objects.filter(order=context['order'])
        context['order_products'] = order_products
        return context
    
@staff_member_required
def order_complete(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.completed = True
    order.save()
    return HttpResponseRedirect(reverse('view_orders'))