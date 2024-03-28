from django.shortcuts import render
from django.views.generic import View
from .models import Contact
from .forms import ContactForm
from django.urls import reverse


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        print(request.POST)
        print(request.META.get('REMOTE_ADDR'))
        form = ContactForm(request.POST)
        if form.is_valid():
            print('valid')
            contact = form.save()
            if contact.email:
                try:
                    print('sending email')
                    contact.send_email()
                    print('email sent')
                except Exception as e:
                    print(f"Error sending email: {e}")
            return render(request, 'contact.html', {'form': form, 'success': True})
        else:
            print('form not valid')
            # Log or print the form errors, especially useful for debugging
            print(form.errors)
        return render(request, 'contact.html', {'form': form})
    
