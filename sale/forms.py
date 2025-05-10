from django import forms
from .models import GoldInvoice,GoldPayment,GoldProduct
from .models import DigiInvoice,DigiPayment,DigiProduct
from accounts.models import Customer





class GoldProductForm(forms.ModelForm):
    class Meta:
        model = GoldProduct
        fields = ['goldcode', 'goldname', 'weight', 'karat', 'sale_ojrat','buy_ojrat', 'seller_benefit',  'daily_price','price']
        widgets = {
            'goldcode': forms.TextInput(attrs={"placeholder": "کد کالا", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'goldname': forms.TextInput(attrs={"placeholder": "نام کالا", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'weight': forms.NumberInput(attrs={"placeholder": "وزن", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'karat': forms.NumberInput(attrs={"placeholder": "عیار", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'sale_ojrat': forms.NumberInput(attrs={"placeholder": "اجرت فروش", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'buy_ojrat': forms.NumberInput(attrs={"placeholder": "اجرت خرید", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'seller_benefit': forms.NumberInput(attrs={"placeholder": "سود فروشنده", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'daily_price': forms.NumberInput(attrs={"placeholder": "قیمت روز طلا (تومان)", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'price': forms.NumberInput(attrs={"placeholder": "قیمت کالا", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),

        }
        labels = {
            'goldcode': '',
            'goldname': '',
            'weight': '',
            'karat': '',
            'sale_ojrat': '',
            'buy_ojrat': '',
            'seller_benefit': '',
            'daily_price': '',
            'price': '',

        }

    def __init__(self, *args, **kwargs):
        super(GoldProductForm, self).__init__(*args, **kwargs)
        # اجباری کردن فیلدها به صورت جداگانه
        self.fields['goldcode'].required = True
        self.fields['goldname'].required = True
        self.fields['weight'].required = True
        self.fields['karat'].required = True
        self.fields['sale_ojrat'].required = True
        self.fields['buy_ojrat'].required = True
        self.fields['seller_benefit'].required = True
        self.fields['daily_price'].required = True
        self.fields['price'].required = True

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight is not None and weight <= 0:
            raise forms.ValidationError("وزن را درست وارد نمایید")
        return weight
# ------------------------------------------------

class GoldInvoiceForm(forms.ModelForm):
    class Meta:
        model = GoldInvoice
        fields = [ 'date','customersale','seller' ]
        widgets = {
            'seller': forms.Select(attrs={'class': 'form-control','style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',}),
            'customersale': forms.Select(
                attrs={'class': 'form-control select2', 'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;', }),
            'date': forms.TextInput(attrs={'data-jdp': 'true',
                'class': 'form-control',
                'required': True,
                'placeholder': 'تاریخ فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 13px;', 'autocomplete': 'off',
                 # اضافه کردن این خط
            }),
        }
        labels = {
            'seller': 'فروشنده',
            'customersale': 'مشتری',
            'date': '',
        }

# -------------------------------------------
class GoldPaymentForm(forms.ModelForm):
    class Meta:
        model = GoldPayment
        fields = [ 'amount', 'pay_date','payment_explain','discount','discount_code','etebar','etebar_code', 'payment_method']
        widgets = {
            'amount': forms.NumberInput(attrs={"placeholder": "مبلغ پرداخت", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'pay_date': forms.TextInput(attrs={'data-jdp': 'true','class': 'form-control','required': True,"placeholder": "تاریخ پرداخت" , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px", 'autocomplete': 'off'}),
            'payment_explain':forms.TextInput(attrs={"placeholder": "شرح پرداخت", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'discount': forms.NumberInput(attrs={"placeholder":"تخفیف" , "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'discount_code': forms.TextInput(attrs={"placeholder": "کد تخفیف", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'etebar': forms.NumberInput(
                attrs={"placeholder": "اعتبار", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'etebar_code': forms.TextInput(
                attrs={"placeholder": "کد اعتبار", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'payment_method': forms.Select(attrs={'class': 'form-control', "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
        }
        labels = {
            'amount': '',
            'pay_date': '',
            'payment_explain':'',
            'discount': '',
            'discount_code': '',
            'etebar': '',
            'etebar_code': '',
            'payment_method': 'روش پرداخت',
        }

# ============================DIGITAL======================
class DigiProductForm(forms.ModelForm):
    class Meta:
        model = DigiProduct
        fields = ['digicode', 'diginame', 'brand', 'model', 'color','qty', 'unit_price']
        widgets = {
            'digicode': forms.TextInput(attrs={"placeholder": "کد کالا", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'diginame': forms.TextInput(attrs={"placeholder": "نام کالا", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'brand': forms.TextInput(attrs={"placeholder": "برند", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'model': forms.TextInput(attrs={"placeholder": "مدل", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'color': forms.TextInput(attrs={"placeholder": "رنگ", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'qty': forms.NumberInput(attrs={"placeholder": "تعداد", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'unit_price': forms.NumberInput(attrs={"placeholder": "قیمت واحد", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),

        }
        labels = {
            'digicode': '',
            'diginame': '',
            'brand': '',
            'model': '',
            'color': '',
            'qty': '',
            'unit_price': '',
        }

    def __init__(self, *args, **kwargs):
        super(DigiProductForm, self).__init__(*args, **kwargs)
        # اجباری کردن تمام فیلدها
        self.fields['digicode'].required = True
        self.fields['diginame'].required = True
        self.fields['brand'].required = True
        self.fields['model'].required = True
        self.fields['color'].required = True
        self.fields['qty'].required = True
        self.fields['unit_price'].required = True

    def clean_qty(self):
        qty = self.cleaned_data.get('qty')
        if qty is not None and qty <= 0:
            raise forms.ValidationError("تعداد را درست وارد نمایید")
        return qty
# -----------------------------------------------
class DigiInvoiceForm(forms.ModelForm):
    class Meta:
        model = DigiInvoice
        fields = [ 'date','customersale','seller' ]
        widgets = {
            'seller': forms.Select(
                attrs={'class': 'form-control', 'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;', }),
            'customersale': forms.Select(
                attrs={'class': 'form-control', 'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;', }),
            'date': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True,
                'placeholder': 'تاریخ فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 13px;', 'autocomplete': 'off',
                'data-jdp': 'true',  # اضافه کردن این خط
            }),
        }
        labels = {
            'seller': 'فروشنده',
            'customersale': 'مشتری',
            'date': '',
        }
# ---------------------------------------------
class DigiPaymentForm(forms.ModelForm):
    class Meta:
        model = DigiPayment
        fields = [ 'digiamount', 'pay_date','payment_explain','digidiscount','discount_code','etebar','etebar_code' ,'payment_method']
        widgets = {
            'digiamount': forms.NumberInput(attrs={"placeholder": "مبلغ پرداخت", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'pay_date': forms.TextInput(attrs={'data-jdp': 'true','class': 'form-control','required': True,"placeholder": "تاریخ پرداخت" , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px", 'autocomplete': 'off'}),
            'payment_explain':forms.TextInput(attrs={"placeholder": "شرح پرداخت", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'digidiscount': forms.NumberInput(attrs={"placeholder":"تخفیف" , "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'discount_code': forms.TextInput(attrs={"placeholder": "کد تخفیف", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'etebar': forms.NumberInput(
                attrs={"placeholder": "اعتبار", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'etebar_code': forms.TextInput(
                attrs={"placeholder": "کد اعتبار", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'payment_method': forms.Select(attrs={'class': 'form-control', 'required': True, "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
        }
        labels = {
            'digiamount': '',
            'pay_date': '',
            'payment_explain':'',
            'digidiscount': '',
            'discount_code': '',
            'etebar': '',
            'etebar_code': '',
            'payment_method': 'روش پرداخت',
        }
