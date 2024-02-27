from .models import Contact
from django import forms

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'order_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg-kate-200'}),
            'email': forms.EmailInput(attrs={'class': 'bg-kate-200'}),
            'message': forms.Textarea(attrs={'class': 'bg-kate-200'}),
            'order_number': forms.TextInput(attrs={'class': 'bg-kate-200'}),
        }