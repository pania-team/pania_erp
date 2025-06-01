from django import forms
from .models import Lead, Product, Tag
from django_jalali.forms import jDateField
import jdatetime


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['type', 'brand', 'model_name']
        widgets = {
            'type': forms.Select(attrs={
                'class': 'form-control',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'برند',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
            'model_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مدل کالا',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
        }
        labels = {
            'type': 'نوع کالا',
            'brand': '',
            'model_name': '',
        }


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'mellicode', 'phone', 'phone_number', 
                 'source', 'city', 'requested_products', 'tags']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
            'mellicode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'کد ملی',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره ثابت',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'تلفن همراه',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px',
                'required': True
            }),
            'source': forms.Select(attrs={
                'class': 'form-control',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شهر',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
            'requested_products': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control select2',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
            }),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'mellicode': '',
            'phone': '',
            'phone_number': '',
            'source': '',
            'city': '',
            'requested_products': '',
            'tags': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].empty_label = 'منبع را انتخاب کنید'
        self.fields['requested_products'].widget.attrs.update({
            'data-placeholder': 'کالاهای درخواستی را انتخاب کنید'
        })
        self.fields['tags'].widget.attrs.update({
            'data-placeholder': 'تگ‌ها را انتخاب کنید'
        })
        
        # Check if there are any products
        if not Product.objects.exists():
            self.fields['requested_products'].widget.attrs.update({
                'disabled': 'disabled'
            })
            self.fields['requested_products'].help_text = 'هیچ کالایی موجود نیست. لطفا ابتدا یک کالا ایجاد کنید.'