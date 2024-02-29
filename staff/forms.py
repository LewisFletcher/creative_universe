from django import forms


class CustomEmailForm(forms.Form):
    subject = forms.CharField(
        max_length=100,
        initial="A message from Creative Universe Productions",
        widget=forms.TextInput(attrs={'class': 'bg-kate-200'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'bg-kate-200'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'bg-kate-200'})
    )

class ShippingEmailForm(forms.Form):
    subject = forms.CharField(max_length=100, initial="Your order has shipped!", widget=forms.TextInput(attrs={'class': 'bg-kate-200'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'bg-kate-200'}))
    tracking_number = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'bg-kate-200'}))
    carrier = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'bg-kate-200'}))
    message = forms.CharField(initial="Your order has shipped! Here is your tracking number: ", widget=forms.Textarea(attrs={'class': 'bg-kate-200'}))