from django.views.generic.base import View
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse_lazy, reverse
import stripe
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView
from .models import Price, Product, Order, Customer, ShippingAddress, OrderProduct
from django.utils.html import mark_safe
from django.db.models import Q
from datetime import datetime, timedelta
from artpage.models import ArtPiece, Print, Sticker, PhotographyPrints, Merch
from itertools import chain
from operator import attrgetter
from django.apps import apps
# Create your views here.

def get_mixed_latest_items():
    # Fetch more than 9 from each to ensure a good mix
    art_pieces = ArtPiece.objects.filter(Q(total_stock__gt=0) | Q(total_stock__isnull=True)).order_by('-uploaded')
    prints = Print.objects.filter(Q(total_stock__gt=0) | Q(total_stock__isnull=True)).order_by('-uploaded')
    stickers = Sticker.objects.filter(Q(total_stock__gt=0) | Q(total_stock__isnull=True)).order_by('-uploaded')
    photography_prints = PhotographyPrints.objects.filter(Q(total_stock__gt=0) | Q(total_stock__isnull=True)).order_by('-uploaded')
    merchs = Merch.objects.filter(Q(total_stock__gt=0) | Q(total_stock__isnull=True)).order_by('-uploaded')

    # Combine all the items into one big list
    combined_items = list(chain(art_pieces, prints, stickers, photography_prints, merchs))

    # Sort the combined list by 'uploaded' date and get the top nine items
    latest_items = sorted(combined_items, key=attrgetter('uploaded'), reverse=True)

    return latest_items


class ShopView(ListView):
    template_name = 'shop.html'
    context_object_name = 'items'
    paginate_by = 9
    
    def get_template_names(self):
        if self.request.htmx:
            return 'shop_loop.html'
        return 'shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url"] = self.request.path
        if category := self.request.GET.get('category'):
            if category == 'originals':
                model_name = 'ArtPiece'
                context['category'] = 'Originals'
            if category == 'prints':
                model_name = 'Print'
                context['category'] = 'Prints'
            if category == 'stickers':
                model_name = 'Sticker'
                context['category'] = 'Stickers'
            if category == 'photography_prints':
                model_name = 'PhotographyPrints'
                context['category'] = 'Photography Prints'
            if category == 'merch':
                model_name = 'Merch'
                context['category'] = model_name
        return context
    
    def get_queryset(self):
        queryset = get_mixed_latest_items()
        if category := self.request.GET.get('category'):
            if category == 'originals':
                model_name = 'ArtPiece'
            if category == 'prints':
                model_name = 'Print'
            if category == 'stickers':
                model_name = 'Sticker'
            if category == 'photography_prints':
                model_name = 'PhotographyPrints'
            if category == 'merch':
                model_name = 'Merch'
            model = apps.get_model('artpage', model_name)
            queryset = model.objects.filter(Q(total_stock__gt=0) | Q(total_stock__isnull=True)).order_by('-uploaded')
        return queryset

    
def add_to_cart(request, item_id, model_name):
    cart = request.session.get('cart', {})
    item_key = f"{model_name}_{item_id}"
    if item_key in cart:
        return render(request, 'cart_button.html', {'cart': cart})
    cart[item_key] = cart.get(item_key, 0) + 1
    request.session['cart'] = cart

    if 'HX-Request' in request.headers:
        return render(request, 'cart_button.html', {'cart': cart})
    else:
        return redirect('view_cart')

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    if cart.get(item_id):
        cart[item_id] -= 1
        if cart[item_id] <= 0:
            del cart[item_id]
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for item_key, quantity in cart.items():
        model_name, item_id = item_key.split('_')
        model = apps.get_model('artpage', model_name)
        item = get_object_or_404(model, pk=item_id)
        price = item.product.prices.first().price
        total += price * quantity
        items.append((item, quantity))
    print(items)
    return render(request, 'cart.html', {'items': items, 'total': total})

def update_cart(request, model_name, item_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 0))
    item_key = f"{model_name}_{item_id}"
    if quantity <= 0:
        del cart[item_key]
    else:
        cart[item_key] = quantity
    request.session['cart'] = cart
    items = []
    total = 0
    for item_key, quantity in cart.items():
        model_name, item_id = item_key.split('_')
        model = apps.get_model('artpage', model_name)
        item = get_object_or_404(model, pk=item_id)
        price = item.product.prices.first().price
        total += price * quantity
        items.append((item, quantity))
    return render(request, 'cart_items.html', {'items': items, 'total': total})

def create_stripe_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    cart = request.session.get('cart', {})
    success_url = request.build_absolute_uri(reverse('payment_success'))
    cancel_url = request.build_absolute_uri(reverse('payment_cancelled'))
    line_items = []

    if 'order_id' in request.session:
        order = Order.objects.get(id=request.session['order_id'])
        if order.status == False:
            order.delete()
        del request.session['order_id']
    
    total = 0
    for item_key, quantity in cart.items():
        model_name, item_id = item_key.split('_')
        model = apps.get_model('artpage', model_name)
        item = get_object_or_404(model, pk=item_id)
        price = item.product.prices.first()
        total += price.price * quantity
        line_items.append({
            'quantity': quantity,
            'price' : price.stripe_price_id
        })
    order = Order.objects.create(status=False, total=total, order_id=Order.generate_order_id())
    order_id = order.id
    request.session['order_id'] = order_id
    for item_key, quantity in cart.items():
        model_name, item_id = item_key.split('_')
        model = apps.get_model('artpage', model_name)
        item = get_object_or_404(model, pk=item_id)
        price = item.product.prices.first()

        OrderProduct.objects.create(
            product=item.product,
            price=price,
            order=order,
            quantity=quantity,
            item_key=item_key
        )
    session = stripe.checkout.Session.create(
        payment_intent_data={
                'metadata' : {'order_id': order_id}
            },
            metadata={
                "order_id": order_id,
            },
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        automatic_tax={'enabled': True},
        billing_address_collection='auto',
        shipping_address_collection={'allowed_countries': ['US', 'CA']},
        phone_number_collection={'enabled': True},
    )
    return redirect(session.url, code=303)

def payment_success(request):
    print(request.session.get('order_id'))
    order = Order.objects.get(
        id=request.session.get('order_id')
    )
    request.session['cart'] = {}
    items = []
    for order_product in order.orderproduct_set.all():
        model_name, item_id = order_product.item_key.split('_')
        model = apps.get_model('artpage', model_name)
        item = get_object_or_404(model, pk=item_id)
        if item.total_stock is not None:
            item.total_stock -= order_product.quantity
            item.save()
            print(item.total_stock)
        items.append((item, order_product.quantity))
    return render(request, 'payment_success.html', {'order': order, 'items': items, 'total': order.total, 'order_id': order.order_id})

@csrf_exempt
def payment_webhook(request):
    payload = request.body
    print(payload)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order = Order.objects.get(order_id=session['order_id'])
        order.stripe_order_id = session['id']
        order.customer_paid = session['amount_total']
        order.status = True
        order.save()
        print('Payment was successful.')
    return HttpResponse(status=200)

def payment_cancelled(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for item_key, quantity in cart.items():
        model_name, item_id = item_key.split('_')
        model = apps.get_model('artpage', model_name)
        item = get_object_or_404(model, pk=item_id)
        price = item.product.prices.first().price
        total += price * quantity
        items.append((item, quantity))
    print(items)
    return render(request, 'cart.html', {'items': items, 'total': total, 'cancelled': True})

