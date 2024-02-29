from django.db import models
from artpage.models import ArtPiece
# Create your models here.

class ShippingAddress(models.Model):
    name = models.CharField(
        "Full name",
        max_length=1024,
    )

    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    country = models.CharField(
        "Country",
        max_length=3,
    )

class Customer(models.Model):
    first_name = models.CharField(max_length=200, null=False)
    last_name = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(ShippingAddress, on_delete=models.PROTECT)

    def __str__(self):
        return self.last_name

class Product(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    stripe_product_id = models.CharField(max_length=100)
    product_description = models.CharField(max_length=300, null=True)

    def get_price(self):
        return self.prices.first().price

    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices")
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    price_description = models.CharField(max_length=300, null=True)

    class Meta:
        ordering = ['price']
	
    def get_display_price(self):
        return "{0:.2f}".format(self.price)

    def __str__(self):
        return '%s %s %s %s' % ("$", self.price, "-", self.price_description)
    
class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    item_key = models.CharField(max_length=100, null=True)

    def get_total_price(self):
        return self.quantity * self.product.get_price()

    def __str__(self):
        return self.product.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cust_details', null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)
    status = models.BooleanField(default= False)
    stripe_order_id = models.CharField(max_length=100, null=True)
    fullfilment_date = models.DateTimeField(null=True)
    order_id = models.CharField(max_length=100, null=True)
    total = models.FloatField(default= 0)

    def send_confirmation_email(self):
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags

        items = {}
        for item in self.orderproduct_set.all():
            items[f"{item.product.name} x {item.quantity}" ] = item.get_total_price()

        html_content = render_to_string('order_confirmation_email.html', {'order': self, 'items': items})
        plain_message = strip_tags(html_content)

        send_mail(
            subject='Order Confirmation',
            message=plain_message,
            from_email="orders@creativeuniverseproductions.com",
            recipient_list=[self.email],
            html_message=html_content,
            fail_silently=False,
        )

        staff_html_content = render_to_string('staff_order_email.html', {'order': self, 'items': items})
        staff_plain_message = strip_tags(staff_html_content)

        send_mail(
            subject='New order',
            message=staff_plain_message,
            from_email="orders@creativeuniverseproductions.com",
            recipient_list=["KatelynS80@gmail.com"],
            html_message=staff_html_content,
            fail_silently=False,
        )

    def generate_order_id():
        import datetime
        last_order = Order.objects.all().order_by('id').last()

        if not last_order or 'ORD-' not in last_order.order_id:
            return f'ORD-1'

        # Extract the numeric part of the order_id
        parts = last_order.order_id.split('-')
        if len(parts) > 1 and parts[1].isdigit():
            order_number = int(parts[1]) + 1
        else:
            order_number = 1

        new_order_id = f'ORD-{order_number}'
        return new_order_id

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        return super().save(*args, **kwargs)