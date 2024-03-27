from .models import Contact
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'order_number', 'captcha']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'bg-kate-200'}),
            'email': forms.EmailInput(attrs={'class': 'bg-kate-200'}),
            'message': forms.Textarea(attrs={'class': 'bg-kate-200'}),
            'order_number': forms.TextInput(attrs={'class': 'bg-kate-200'}),
        }

