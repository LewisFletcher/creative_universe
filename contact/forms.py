from .models import Contact
from django import forms

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'order_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'text-black'}),
            'email': forms.EmailInput(attrs={'class': 'text-black'}),
            'message': forms.Textarea(attrs={'class': 'text-black'}),
            'order_number': forms.TextInput(attrs={'class': 'text-black'}),
        }