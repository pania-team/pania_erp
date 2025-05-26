from django import forms
from .models import SaleInvoice,BuyInvoice,BuyItem
from accounts.models import Customer,Supplier
from django_select2.forms import ModelSelect2Widget








class BuyInvoiceForm(forms.ModelForm):
    class Meta:
        model =BuyInvoice
        fields = [ 'supplier','date','total_amount','discount_amount','note' ]
        widgets = {

            'supplier': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'date': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'تاریخ فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 13px;', 'autocomplete': 'off',
                'data-jdp': 'true',  # اضافه کردن این خط
            }),
            'total_amount': forms.NumberInput(attrs={
                "placeholder": "مبلغ فاکتور",
                'required': True,
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;"
            }),
            'discount_amount': forms.NumberInput(attrs={
                "placeholder": "تخفیف",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;"
            }),
            'note': forms.TextInput(attrs={
                "placeholder": "توضیحات",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;"
            }),
        }
        labels = {
            'supplier': '',
            'discount_amount': '',
            'date': '',
            'total_amount': '',
            'note': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # این قسمت باعث می‌شود فیلدها با وجود default در مدل، در فرم خالی نمایش داده شوند
        self.fields['discount_amount'].initial = None
        self.fields['total_amount'].initial = None

# --------------------------------------------------
class BuyItemForm(forms.ModelForm):
    class Meta:
        model =BuyItem
        fields = ['item', 'quantity', 'unit_price', 'tax', 'discount_kala']
        widgets = {
            'item': forms.Select(attrs={
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required',
                'class': 'select2',  # اضافه شود
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'تعداد',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'قیمت واحد',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),
            'tax': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'مالیات کالا',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'discount_kala': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'تخفیف کالا(تومان)',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),

        }
        labels = {
            'item': '',
            'quantity': '',
            'unit_price': '',
            'tax': '',
            'discount_kala': '',
        }
# ---------------------------------------
class UploadImageForm(forms.Form):
    image = forms.ImageField(label="", required=True)