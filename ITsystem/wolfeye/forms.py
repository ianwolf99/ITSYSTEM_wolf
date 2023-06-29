from django import forms
from .models import CustomUser, FinancialInfo

class IPAddressForm(forms.Form):
    ip_address = forms.GenericIPAddressField()
    smb_scan = forms.BooleanField(required=False)
    smtp_scan = forms.BooleanField(required=False)
    ssh_scan = forms.BooleanField(required=False)
    http_scan = forms.BooleanField(required=False)
    wordpress_scan = forms.BooleanField(required=False)
    zimbra_scan = forms.BooleanField(required=False)
    vmware_scan = forms.BooleanField(required=False)
"""
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
"""
class FinancialInfoForm(forms.ModelForm):
    class Meta:
        model = FinancialInfo
        fields = ['credit_card_number', 'expiration_month', 'expiration_year', 'cvv']
