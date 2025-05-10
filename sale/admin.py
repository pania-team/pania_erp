from django.contrib import admin
from .models import   GoldInvoice, GoldPayment, GoldProduct
from .models import  DigiInvoice, DigiPayment, DigiProduct
from django import forms





# =======================GOLD=================================

@admin.register(GoldInvoice)
class GoldInvoiceAdmin(admin.ModelAdmin):
    list_display = ('customersale',  'date', 'status', 'formatted_total_amount','formatted_total_paid','seller')
    search_fields = ('customersale__first_name', 'customersale__last_name', 'seller__name')
    list_filter = ('status', 'date','seller')
    date_hierarchy = 'date'

    def formatted_total_amount(self, obj):
        return f"{obj.total_amount:,}"  # نمایش قیمت بصورت سه تایی اعداد
    formatted_total_amount.short_description = 'جمع مبلغ فاکتور'


    def formatted_total_paid(self, obj):
        return f"{obj.total_paid:,}"  # نمایش قیمت بصورت سه تایی اعداد
    formatted_total_paid.short_description = 'جمع پرداختی مشتری'

# -----------------------------------------------
@admin.register(GoldProduct)
class GoldProductAdmin(admin.ModelAdmin):
    list_display = ('goldcode', 'goldname', 'customer_name')  # اضافه کردن نام مشتری
    search_fields = ('goldcode', 'goldname', 'goldinvoice__customersale__first_name', 'goldinvoice__customersale__last_name')  # امکان جستجو بر اساس نام مشتری

    # متد برای دریافت نام مشتری از فاکتور طلا
    def customer_name(self, obj):
        if obj.goldinvoice and obj.goldinvoice.customersale:
            return f"{obj.goldinvoice.customersale.first_name} {obj.goldinvoice.customersale.last_name}"
        return "نامشخص"
    customer_name.short_description = 'نام خریدار'




# ---------------------------------------------------------


class GoldPaymentForm(forms.ModelForm):
    class Meta:
        model = GoldPayment
        fields = '__all__'
        widgets = {
            'amount': forms.NumberInput(attrs={'style': 'width: 150px;'}),  # تعیین طول بیشتر برای مبلغ پرداخت
            'etebar': forms.NumberInput(attrs={'style': 'width: 150px;'}),
            'discount': forms.NumberInput(attrs={'style': 'width: 150px;'}),  # تعیین طول بیشتر برای تخفیف
            'discount_code': forms.TextInput(attrs={'style': 'width: 150px;'}),  # تعیین طول بیشتر برای کد تخفیف
            'etebar_code': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'payment_explain': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'payment_method': forms.TextInput(attrs={'style': 'width: 150px;'}),
        }



@admin.register(GoldPayment)
class GoldPaymentAdmin(admin.ModelAdmin):
    list_display = ('goldinvoice', 'pay_date', 'payment_method','formatted_amount','formatted_discount','discount_code')
    search_fields = ('goldinvoice__id', 'goldinvoice__customersale__first_name', 'goldinvoice__customersale__last_name')
    list_filter = ('payment_method', 'pay_date')
    date_hierarchy = 'pay_date'
    form = GoldPaymentForm

    def formatted_amount(self, obj):
        return f"{obj.amount:,}"  # فرمت‌بندی تخفیف به صورت سه‌تایی
    formatted_amount.short_description = 'جمع پرداختی مشتری'

    def formatted_discount(self, obj):
        if obj.discount is not None:
            return f"{obj.discount:,}"  # فرمت‌بندی تخفیف به صورت سه‌تایی
        return "0"  # فرمت‌بندی تخفیف به صورت سه‌تایی
    formatted_discount.short_description = 'تخفیف'




# =========================== DIGITAL ======================================

@admin.register(DigiInvoice)
class DigiInvoiceAdmin(admin.ModelAdmin):
    list_display = ('customersale', 'date', 'status', 'formatted_total_digiamount', 'formatted_total_digipaid', 'seller')
    search_fields = ('customersale__first_name', 'customersale__last_name', 'seller__name')
    list_filter = ('status', 'date', 'seller')
    date_hierarchy = 'date'

    def formatted_total_digiamount(self, obj):
        return f"{obj.total_digiprice:,}"  # نمایش قیمت بصورت سه تایی اعداد
    formatted_total_digiamount.short_description = 'جمع مبلغ فاکتور'


    def formatted_total_digipaid(self, obj):
        return f"{obj.total_digipaid:,}"  # نمایش قیمت بصورت سه تایی اعداد
    formatted_total_digipaid.short_description = 'جمع پرداختی مشتری'


# -----------------------------------------------
@admin.register(DigiProduct)
class DigiProductAdmin(admin.ModelAdmin):
    list_display = ('digicode','qty','unit_price' ,'formatted_digiprice' ,'diginame','color', 'customer_name')  # اضافه کردن نام مشتری
    search_fields = ('digicode','qty' ,'unit_price' ,'formatted_digiprice' ,'diginame','color', 'digiinvoice__customersale__first_name', 'digiinvoice__customersale__last_name')  # امکان جستجو بر اساس نام مشتری

    def customer_name(self, obj):
        if obj.digiinvoice and obj.digiinvoice.customersale:
            return f"{obj.digiinvoice.customersale.first_name} {obj.digiinvoice.customersale.last_name}"
        return "نامشخص"
    customer_name.short_description = 'نام خریدار'

    def formatted_digiprice(self, obj):
        return f"{obj.digiprice:,}"
    formatted_digiprice.short_description = 'قیمت فروش'

# ---------------------------------------------------------
class DigiPaymentForm(forms.ModelForm):
    class Meta:
        model = DigiPayment
        fields = '__all__'
        widgets = {
            'digiamount': forms.NumberInput(attrs={'style': 'width: 150px;'}),  # تعیین طول بیشتر برای مبلغ پرداخت
            'etebar': forms.NumberInput(attrs={'style': 'width: 150px;'}),
            'digidiscount': forms.NumberInput(attrs={'style': 'width: 150px;'}),  # تعیین طول بیشتر برای تخفیف
            'discount_code': forms.TextInput(attrs={'style': 'width: 150px;'}),  # تعیین طول بیشتر برای کد تخفیف
            'etebar_code': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'payment_explain': forms.TextInput(attrs={'style': 'width: 150px;'}),
            'payment_method': forms.TextInput(attrs={'style': 'width: 150px;'}),
        }


@admin.register(DigiPayment)
class DigiPaymentAdmin(admin.ModelAdmin):
    list_display = (
    'digiinvoice', 'pay_date', 'payment_method', 'formatted_digiamount', 'formatted_digidiscount', 'discount_code')
    search_fields = ('digiinvoice__id', 'digiinvoice__customersale__first_name', 'digiinvoice__customersale__last_name')
    list_filter = ('payment_method', 'pay_date')
    date_hierarchy = 'pay_date'
    form = DigiPaymentForm

    def formatted_digiamount(self, obj):
        return f"{obj.digiamount:,}"  # فرمت‌بندی تخفیف به صورت سه‌تایی
    formatted_digiamount.short_description = 'جمع پرداختی مشتری'


    def formatted_digidiscount(self, obj):
        if obj.digidiscount is not None:
            return f"{obj.digidiscount:,}"  # فرمت‌بندی تخفیف به صورت سه‌تایی
        return "0"
    formatted_digidiscount.short_description = 'تخفیف'
