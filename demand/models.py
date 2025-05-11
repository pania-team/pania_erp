
from django.conf import settings
from django.db import models
from django_jalali.db import models as jmodels
from django.utils import timezone
from accounts.models import Customer







  # مدل وام
class Loan(models.Model):
    PLAN_CHOICES = [
        ('', ''),
        ('آزاد', 'آزاد'),
        ('بتا', 'بتا'),
        ('سازمانی', 'سازمانی'),
        ('نمایندگی', 'نمایندگی'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans',verbose_name='مشتری')
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='none', verbose_name='طرح وام')
    loan_code = models.CharField(max_length=20,null=True, blank=True, verbose_name='کد وام')
    total_amount = models.BigIntegerField(verbose_name='مبلغ اصل وام')
    final_amount = models.BigIntegerField( verbose_name='بازپرداخت نهایی')
    loan_date = jmodels.jDateField(verbose_name='تاریخ اخذ وام', null=True, blank=True)
    start_date = jmodels.jDateField(verbose_name='تاریخ اولین قسط', null=True, blank=True)
    end_date = jmodels.jDateField(verbose_name= 'تاریخ آخرین قسط' , null=True, blank=True)
    num_month = models.PositiveIntegerField( verbose_name='مدت وام(ماه)' , null=True, blank=True)
    num_installments = models.PositiveIntegerField(verbose_name='تعداد بازپرداخت' , null=True, blank=True)
    total_received_customer = models.BigIntegerField(default=0, verbose_name='جمع پرداختی مشتری')
    loan_mande_bedehi = models.BigIntegerField(default=0, verbose_name='مانده بدهی وام')
    installments_created = models.BooleanField(default=False)
    tasviye_status = models.BooleanField(default=False, verbose_name="وضعیت تسویه")

    def __str__(self):
        return f" {self.customer.first_name} {self.customer.last_name} "
    class Meta:
        verbose_name = 'وام'
        verbose_name_plural = 'وامها'

  # محاسبه مانده معوق
    def calculate_mande_moavagh(self):
        now_date = timezone.now().date()
        total_mande_moavagh = 0
        for installment in self.installments.all():
            if installment.due_date and installment.due_date < now_date and not installment.paid:
                mande_moavagh_amount = installment.amount - installment.total_ghest_repaid
                total_mande_moavagh += mande_moavagh_amount
        return total_mande_moavagh


# ----------------------------------------------------
# مدل قسط
class Installment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='installments',verbose_name='مشتری')
    ghest_count = models.PositiveIntegerField(default=0, verbose_name='شماره قسط')
    amount = models.PositiveIntegerField(verbose_name='مبلغ قسط', null=True, blank=True)
    due_date = jmodels.jDateField(verbose_name='تاریخ سررسید', null=True, blank=True)
    paid = models.BooleanField(default=False,verbose_name='وضعیت پرداخت')
    ghest_type = models.CharField(max_length=50,null=True, blank=True,
                                      choices=[('نقدی', 'نقدی'), ('بتا', 'بتا'), ('چک', 'چک'),('نمایندگی','نمایندگی')], verbose_name='نوع قسط')
    ghest_place = models.CharField(max_length=50,null=True, blank=True,verbose_name='محل وصول قسط')
    total_ghest_repaid = models.PositiveIntegerField(default=0, verbose_name='جمع بازپرداخت‌ هر قسط')
    penalty_amount = models.PositiveIntegerField(verbose_name='دیرکرد هر قسط', default=0)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    def __str__(self):
        return f" {self.loan.customer.first_name} {self.loan.customer.last_name}"
    class Meta:
        verbose_name = 'مطالبات'
        verbose_name_plural = 'مطالبات'
    # مانده معوق قسط
    def calculate_mande_moavagh_ghest(self):
        mande_moavagh_ghest = self.amount - self.total_ghest_repaid
        return mande_moavagh_ghest


# --------------------------------------------------

class Repayment(models.Model):
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE, related_name='repayments')
    repayment_amount = models.PositiveIntegerField( verbose_name='بازپرداخت قسط')
    repayment_date = jmodels.jDateField( null=True, blank=True ,verbose_name='تاریخ بازپرداخت') # اضافه شده
    payment_method = models.CharField(max_length=20, verbose_name='نحوه پرداخت',null=True, blank=True, choices=[('cash', 'واریز به حساب'), ('chek', 'چک'),('link', 'لینک')])
    payment_voucher = models.CharField(max_length=100, verbose_name='رسید پرداخت', null=True, blank=True) # اضافه شده
    payment_place = models.CharField(max_length=20, verbose_name='محل  پرداخت', null=True, blank=True,
                                      choices=[('رفاه', 'رفاه '),('سپه', 'سپه '), ('ملت', 'ملت '), ('پست بانک', 'پست بانک'),('صادرات', 'صادرات'),('تجارت', 'تجارت'),('سایر', 'سایر')])
    created_at = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.installment.loan.customer.first_name} {self.installment.loan.customer.last_name}"
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداختها'

# -----------------------------------------------
    # مدل ضمانت
class Guarantee(models.Model):
    GUARANTEE_TYPE_CHOICES = [
        ('check', 'چک'),
        ('safte', 'سفته'),
    ]
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='guarantees', verbose_name='وام')
    guarantor_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='نام ضامن')
    guarantee_amount = models.PositiveIntegerField(null=True, blank=True,verbose_name='مبلغ ضمانت')
    guarantee_serial = models.CharField(max_length=100, verbose_name='سریال تضامین', null=True, blank=True)
    guarantee_type = models.CharField(max_length=20, choices=GUARANTEE_TYPE_CHOICES, verbose_name='نوع ضمانت', null=True, blank=True)
    guarantee_date = jmodels.jDateField(verbose_name='تاریخ ضمانت', null=True, blank=True)
    guarantor_address = models.CharField(max_length=255, verbose_name='آدرس ضامن', null=True, blank=True)
    guarantor_address2 = models.CharField(max_length=255, verbose_name='آدرس محل کار', null=True, blank=True)
    guarantor_phone = models.CharField(max_length=15, verbose_name='شماره تماس ضامن', null=True, blank=True)
    guarantor_phone2 = models.CharField(max_length=15, verbose_name='شماره تماس 2', null=True, blank=True)
    guarantor_phone3 = models.CharField(max_length=15, verbose_name='شماره تماس ثابت', null=True, blank=True)
    guarantor_mellicod = models.CharField(max_length=10, verbose_name='کد ملی ضامن', null=True, blank=True)


    def __str__(self):
        return f"{self.guarantor_name} - {self.guarantee_type}"
    class Meta:
        verbose_name = 'ضامن'
        verbose_name_plural = 'ضمانت'

# ------------------------------------------------------

# مدل تسویه
class LoanSettlement(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='settlements')
    settlement_date = jmodels.jDateField(verbose_name='تاریخ تسویه', null=True, blank=True)    # تاریخ تسویه
    settled_amount = models.DecimalField(max_digits=10, decimal_places=2 , null=True, blank=True,verbose_name='مبلغ تسویه')   # مبلغ تسویه‌شده
    settlement_method = models.CharField(max_length=50, null=True, blank=True,verbose_name='روش تسویه')  # روش تسویه
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,verbose_name='مبلغ جریمه')  # جریمه‌ها
    notes = models.TextField(blank=True, null=True,verbose_name='شرح تسویه')  # یادداشت‌های تسویه
    return_garanti = models.BooleanField(default=False, verbose_name='وضعیت برگشت تضامین')
    return_date = jmodels.jDateField(null=True, blank=True, verbose_name='تاریخ بازگشت تضامین')
    settlement_status = models.BooleanField(default=False, verbose_name='وضعیت تسویه')

    def __str__(self):
        return f"Settlement for Loan {self.loan.id} on {self.settlement_date}"
