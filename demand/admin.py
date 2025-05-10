
from django.contrib import admin
from .models import  Loan, Installment,Repayment
from django_jalali.admin.filters import JDateFieldListFilter
from .models import Guarantee
from accounts.models import Customer
from django import forms
from django.utils.html import format_html


# --------------------------------------------------
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('loan','ghest_count' ,'formatted_amount', 'due_date', 'paid')
    list_filter = (
        ('due_date', JDateFieldListFilter),
        ('paid', admin.BooleanFieldListFilter),
    )
    search_fields = ('loan__customer__first_name', 'loan__customer__last_name',)

    def formatted_amount(self, obj):
        return f"{obj.amount:,}"  # نمایش قیمت بصورت سه تایی اعداد
    formatted_amount.short_description = 'مبلغ قسط'


    def get_search_results(self, request, queryset, search_term):
        if search_term:
            # جستجو بر اساس نام یا نام خانوادگی مشتری
            customer_ids = Customer.objects.filter(
                first_name__icontains=search_term
            ).values_list('id', flat=True) | Customer.objects.filter(
                last_name__icontains=search_term
            ).values_list('id', flat=True)
            queryset = queryset.filter(loan__customer__id__in=customer_ids)
        return super().get_search_results(request, queryset, search_term)


# -------------------------------------------------

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        widgets = {
            'total_amount': forms.NumberInput(attrs={'style': 'width: 110px;'}),
            'final_amount': forms.NumberInput(attrs={'style': 'width: 110px;'}),
            'total_received_customer': forms.NumberInput(attrs={'style': 'width: 110px;'})
        }
# ----------------------------------------------
from django.contrib import admin


class LoanAdmin(admin.ModelAdmin):
    list_display = (
    'customer', 'plan', 'loan_date', 'loan_code', 'formatted_total_amount', 'formatted_total_received_customer',
    'formatted_loan_mande_bedehi', 'num_month', 'num_installments', 'tasviye_status')

    list_filter = (
        'tasviye_status',
    )

    search_fields = ('customer__first_name', 'customer__last_name','loan_code','plan',)

    fields = (
    'customer', 'plan', 'loan_code', 'total_amount', 'final_amount', 'loan_date', 'start_date', 'end_date', 'num_month',
    'num_installments', 'total_received_customer', 'tasviye_status')
    form = LoanForm

    def formatted_total_amount(self, obj):
        return f"{obj.total_amount:,}"  # نمایش قیمت بصورت سه تایی اعداد

    formatted_total_amount.short_description = 'مبلغ وام'

    def formatted_total_received_customer(self, obj):
        return f"{obj.total_received_customer:,}"

    formatted_total_received_customer.short_description = 'بازپرداخت وام'

    def formatted_loan_mande_bedehi(self, obj):
        return f"{obj.loan_mande_bedehi:,}"

    formatted_loan_mande_bedehi.short_description = 'مانده وام'

    # غیرفعال کردن امکان حذف
    def has_delete_permission(self, request, obj=None):
        return False


# --------------------------------------------------------
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('installment',
                    'get_loan_code',
                    'installment_ghest_count',
                    'paid_status',
                    'installment_amount' ,
                    'format_repayment_amount',
                    'formatted_total_ghest_repaid',
                    'installment_due_date' ,
                    'repayment_date',
                    'payment_method',
                    'payment_voucher')
    list_filter = (
        ('repayment_date', JDateFieldListFilter),
        ('payment_method', admin.ChoicesFieldListFilter),
    )
    search_fields = ('installment__loan__customer__first_name',
                     'installment__loan__customer__last_name',
                     'installment__loan__loan_code',
                     'payment_voucher')
    ordering = ('-created_at',)

    def paid_status(self, obj):
        if obj.installment.paid:
            return format_html('<span style="color: green;">✔️</span>')
        return format_html('<span style="color: red;">❌</span>')
    paid_status.short_description = 'وضعیت پرداخت'  # عنوان ستون در پنل ادمین

    def get_loan_code(self, obj):
        return obj.installment.loan.loan_code if obj.installment and obj.installment.loan else None
    get_loan_code.short_description = 'کد وام'

    def formatted_total_ghest_repaid(self, obj):
        return f"{obj.installment.total_ghest_repaid:,}"  # نمایش قیمت بصورت سه تایی اعداد
    formatted_total_ghest_repaid.short_description = 'جمع بازپرداخت '

    def installment_amount(self, obj):
        return f"{obj.installment.amount:,}"
    installment_amount.short_description = 'مبلغ قسط'

    def format_repayment_amount(self, obj):
        return f"{obj.repayment_amount:,}"
    format_repayment_amount.short_description = 'بازپرداخت قسط'

    def installment_due_date(self, obj):
        return obj.installment.due_date
    installment_due_date.short_description = 'تاریخ قسط'

    def installment_ghest_count(self, obj):
        return obj.installment.ghest_count
    installment_ghest_count.short_description = 'شماره قسط'


# --------------------------------------------------------


class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ('customer_name','guarantor_name', 'formatted_guarantee_amount', 'guarantee_type', 'guarantee_date')
    search_fields = ('loan__customer__first_name','loan__customer__last_name','guarantor_name',  'guarantor_mellicod')
    list_filter = ('guarantee_type',)
    # متد برای دریافت نام مشتری از طریق وام
    def customer_name(self, obj):
        return obj.loan.customer.first_name + ' ' + obj.loan.customer.last_name
    customer_name.short_description = 'وام گیرنده'

    def formatted_guarantee_amount(self, obj):
        if obj.guarantee_amount is not None:  # بررسی وجود مقدار
            return f"{obj.guarantee_amount:,}"  # نمایش قیمت بصورت سه تایی اعداد
        return "0"  # مقدار پیش‌فرض در صورت None
    formatted_guarantee_amount.short_description = 'مبلغ ضمانت'


admin.site.register(Loan, LoanAdmin)
admin.site.register(Installment, InstallmentAdmin)
admin.site.register(Repayment,RepaymentAdmin)
admin.site.register(Guarantee, GuaranteeAdmin)


