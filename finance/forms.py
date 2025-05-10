from django import forms
from sale.models import GoldPayment,DigiPayment





class GoldPaymentConfirmForm(forms.ModelForm):
    class Meta:
        model = GoldPayment
        fields = ['payment_receipt', 'payment_confirm']
        widgets = {
            'payment_receipt': forms.TextInput(attrs={"placeholder": "رسید پرداخت",'required': True,'autocomplete': 'off',"style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'payment_confirm': forms.CheckboxInput(attrs={'required': True,'class': 'form-check-input'}),
        }
        labels = {
            'payment_receipt': '',
            'payment_confirm': 'تأیید پرداخت',
        }

# ----------------------------------------

class DigiPaymentConfirmForm(forms.ModelForm):
    class Meta:
        model = DigiPayment
        fields = ['digipayment_receipt', 'digipayment_confirm']
        widgets = {
            'digipayment_receipt': forms.TextInput(attrs={"placeholder": "رسید پرداخت",'required': True,'autocomplete': 'off',"style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'digipayment_confirm': forms.CheckboxInput(attrs={'required': True,'class': 'form-check-input'}),
        }
        labels = {
            'digipayment_receipt': '',
            'digipayment_confirm': 'تأیید پرداخت',
        }
