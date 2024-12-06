from django import forms
from .models import ShippingAddress
from localflavor.pt.forms import PTZipCodeField, PTRegionSelect
from localflavor.pt.pt_regions import REGION_CHOICES
from phonenumber_field.formfields import PhoneNumberField

class ShippingForm(forms.ModelForm): 
    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nome Completo'}), required=True)
    shipping_phone = PhoneNumberField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nº Telemóvel'}), required=True)
    shipping_email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), required=True)
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Morada'}), required=True)
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nº Porta/Andar/Apartamento'}), required=False)
    shipping_city = forms.ChoiceField(label="", choices=REGION_CHOICES, widget=PTRegionSelect(attrs={'class': 'form-control'}), required=False)
    shipping_zipcode = PTZipCodeField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal'}), required=True)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País'}), required=True, initial='Portugal')
    
    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_phone', 'shipping_email', 'shipping_address1', 
                  'shipping_address2', 'shipping_city', 'shipping_zipcode', 'shipping_country']
        
        exclude = ['user',]
    
class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nome do Proprietário'}), required=True)
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Número do Cartão'}), required=True)
    card_exp_date = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Data de Expiração'}), required=True)
    card_cvv_number = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'CVV2 Número'}), required=True)
    card_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Morada para envio'}), required=True)
    card_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nº Porta/Andar/Apartamento'}), required=True)
    card_city = forms.ChoiceField(label="", choices=REGION_CHOICES, widget=PTRegionSelect(attrs={'class': 'form-control'}), required=True)
    card_zipcode = PTZipCodeField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal (NNNN-NNN)'}), required=True)
    card_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'País do envio'}), required=True, initial="Portugal")