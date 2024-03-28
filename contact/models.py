from django.db import models
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)
# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    order_number = models.CharField(max_length=32, null=True, blank=True, help_text="If you have an order number, please enter it here.")
    date = models.DateTimeField(auto_now_add=True)

    def send_email(self):
        from django.core.mail import send_mail
        
        try:
            html_content = render_to_string('customer_contact_email.html', {'contact': self})
            plain_message = strip_tags(html_content)

            logger.info(f'Sending contact email to {self.email}...')
            customer_email_status = send_mail(
                subject='Thanks for getting in touch!',
                message=plain_message,
                from_email="contact@creativeuniverseproductions.com",
                recipient_list=[self.email],
                html_message=html_content,
                fail_silently=False,
            )
            logger.info(f'Contact email sent to {self.email}. Status: {customer_email_status}')

            staff_html_content = render_to_string('staff_contact_email.html', {'contact': self})
            staff_plain_message = strip_tags(staff_html_content)

            logger.info('Sending contact email to staff...')
            staff_email_status = send_mail(
                subject='New contact form submission',
                message=staff_plain_message,
                from_email="contact@creativeuniverseproductions.com",
                recipient_list=["contact@creativeuniverseproductions.com"],
                html_message=staff_html_content,
                fail_silently=False,
            )
            logger.info(f'Contact email sent to staff. Status: {staff_email_status}')

        except Exception as e:
            logger.error(f'Error sending contact email: {e}', exc_info=True)



    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'