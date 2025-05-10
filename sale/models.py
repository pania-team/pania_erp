from django.db import models
from django_jalali.db import models as jmodels
from django.utils import timezone
from accounts.models import Customer,Seller
from decimal import Decimal





# ========================================GOLD ===========================

#  مدل فاکتور طلا
class GoldInvoice(models.Model):
    customersale = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='goldinvoices', verbose_name='مشتری')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='goldinvoices', verbose_name='فروشنده')
    date = jmodels.jDateField(verbose_name='تاریخ فاکتور', null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True, choices=[('paid', 'پرداخت شده'), ('unfinish', 'ناتمام'), ('cancle', 'لغو')], verbose_name='وضعیت فاکتور')
    total_amount = models.BigIntegerField(verbose_name='مبلغ کل فاکتور', editable=False, default=0)
    total_paid = models.BigIntegerField(default=0, verbose_name='جمع پرداخت‌های مشتری')
    total_weight = models.DecimalField(default=0, max_digits=20, decimal_places=2, verbose_name='جمع وزن فاکتور')
    total_discount = models.BigIntegerField(default=0, verbose_name='تخفیف فاکتور')
    total_calcu_amount = models.BigIntegerField(default=0, verbose_name='جمع مبلغ محاسبه')
    total_remain_amount = models.BigIntegerField(default=0, verbose_name='جمع مبلغ مانده مشتری')
    created_at = jmodels.jDateTimeField(default=timezone.now)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customersale.first_name} {self.customersale.last_name}"

    class Meta:
        verbose_name = 'فاکتور طلا'
        verbose_name_plural = 'فاکتورهای طلا'

    def calculate_total_amount(self):
        total = sum(item.price for item in self.golditems.all())
        return total

    def calculate_total_weight(self):
        total_weight = sum(item.weight for item in self.golditems.all())  # اصلاح شده
        return total_weight

    def calculate_total_discount(self):
        total_discount = sum(payment.discount or 0 for payment in self.payments.all())  # اصلاح شده
        return total_discount

        # جمع مبلغ محاسبه طلا هر فاکتور
    def calculate_total_calcu_amount(self):
        total_calcu_amount = sum(item.calcu_amount for item in self.golditems.all())  # اصلاح شده
        return total_calcu_amount


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total_amount = self.calculate_total_amount()
        self.total_weight = self.calculate_total_weight()
        self.total_discount = self.calculate_total_discount()
        self.total_calcu_amount = self.calculate_total_calcu_amount()
        self.total_remain_amount = self.total_amount - self.total_paid - self.total_discount
        super().save(*args, **kwargs)

    def update_total_paid(self):
        self.total_paid = sum(payment.amount for payment in self.payments.all())
        self.save()

    def refresh_total_remain_amount(self):
        self.total_remain_amount = self.total_amount - self.total_paid - self.total_discount
        self.save()

# -------------------------------------------------------
class GoldProduct(models.Model):
    goldinvoice = models.ForeignKey(GoldInvoice, on_delete=models.CASCADE, related_name='golditems', null=True,verbose_name='فاکتور')
    goldcode = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name='کد کالا')
    goldname = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام کالا')
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='وزن')
    karat = models.PositiveIntegerField(null=True, blank=True,verbose_name='عیار')
    sale_ojrat = models.DecimalField(max_digits=15, decimal_places=1, verbose_name='اجرت فروش')
    buy_ojrat = models.DecimalField(max_digits=15, decimal_places=1,null=True, blank=True, verbose_name='اجرت خرید')
    seller_benefit = models.DecimalField(null=True, blank=True,max_digits=15, decimal_places=1, verbose_name='سود فروشنده')
    sele_benefit = models.DecimalField(null=True, blank=True, max_digits=15, decimal_places=1, verbose_name='سود وزنی فروش')
    sale_tax = models.BigIntegerField( verbose_name='مالیات فروش')
    daily_price = models.BigIntegerField(verbose_name='قیمت روز طلا')
    price = models.BigIntegerField(verbose_name='قیمت فروش کالا')
    calcu_amount = models.BigIntegerField(default=0, verbose_name=' مبلغ محاسبه')
    porsant_value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='پورسانت', default=0)

    def __str__(self):
        return f"طلا - {self.goldname} - {self.weight} گرم"

    class Meta:
        verbose_name = 'محصول طلا'
        verbose_name_plural = 'محصولات طلا'

    # محاسبه سود وزنی کالا
    def calculate_weighted_benefit(self):
        weighted_benefit = self.seller_benefit + (self.sale_ojrat - self.buy_ojrat)
        return weighted_benefit

    def calculate_sale_amount(self):
        j8 = self.weight * (Decimal(1) + (self.sale_ojrat / 100))
        j10 = j8 * (Decimal(1) + (self.seller_benefit / 100))
        j14 =int(j10 * self.daily_price)
        m6 = int(self.weight * Decimal(self.daily_price))
        m10 = int((self.sale_ojrat / 100) * m6)
        m12 = int((m6 + m10) * (self.seller_benefit / 100))
        sale_tax = int((m12 + m10) * Decimal(0.1))  # نرخ مالیات ده درصد
        calcu_amount = int(j14 + sale_tax)  # محاسبه مبلغ فروش
        return calcu_amount, sale_tax

    def save(self, *args, **kwargs):
        # محاسبه سود وزنی و مبلغ فروش
        self.sele_benefit = self.calculate_weighted_benefit()
        self.calcu_amount, self.sale_tax = self.calculate_sale_amount()
        super(GoldProduct, self).save(*args, **kwargs)

# ==============================================
class GoldPayment(models.Model):
    goldinvoice = models.ForeignKey(GoldInvoice, on_delete=models.CASCADE, related_name='payments', verbose_name='فاکتور طلا')
    amount =models.PositiveIntegerField( verbose_name='مبلغ پرداخت')
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='تخفیف ')
    discount_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='کد تخفیف')  # فیلد کد تخفیف
    etebar = models.PositiveIntegerField(null=True, blank=True, verbose_name='اعتبار ')
    etebar_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='کد اعتبار')
    pay_date=jmodels.jDateField(verbose_name='تاریخ پرداخت', null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[('نقدی', 'نقدی'), ('اعتباری', 'اعتباری'),('تهاتر', 'تهاتر')], verbose_name='روش پرداخت')
    payment_explain = models.CharField(max_length=150, null=True, blank=True,verbose_name='شرح پرداخت')
    payment_receipt = models.CharField(max_length=50, null=True, blank=True, verbose_name='رسید پرداخت')
    payment_confirm = models.BooleanField(default=False, verbose_name='تایید پرداخت')

    def __str__(self):
        return f"پرداخت {self.amount} - {self.get_payment_method_display()}"

    class Meta:
        verbose_name = 'پرداخت طلا'
        verbose_name_plural = 'پرداختهای طلا'

# ================================== DIGITAL =======================

#  مدل فاکتوردیجیتال
class DigiInvoice(models.Model):
    customersale = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='digiinvoices', verbose_name='مشتری')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='digiinvoices', verbose_name='فروشنده')
    date = jmodels.jDateField(verbose_name='تاریخ فاکتور', null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True, choices=[('paid', 'پرداخت شده'), ('unfinish', 'ناتمام'), ('cancle', 'لغو')], verbose_name='وضعیت فاکتور')
    total_digiprice = models.BigIntegerField(verbose_name='مبلغ کل فاکتور', editable=False, default=0)
    total_digipaid = models.BigIntegerField(default=0, verbose_name='جمع پرداخت‌های مشتری')
    total_digidiscount = models.BigIntegerField(default=0, verbose_name='تخفیف فاکتور')
    total_digiremain_amount = models.BigIntegerField(default=0, verbose_name='جمع مبلغ مانده مشتری')
    created_at = jmodels.jDateTimeField(default=timezone.now)
    updated_at = jmodels.jDateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customersale.first_name} {self.customersale.last_name}"

    class Meta:
        verbose_name = 'فاکتور دیجیتال'
        verbose_name_plural = 'فاکتورهای دیجیتال'

    def calculate_total_digiprice(self):
        total = sum(item.digiprice for item in self.digiitems.all())
        return total

    def calculate_total_digipaid(self):
        total_digipaid = sum(payment.digiamount for payment in self.digipayments.all())
        return total_digipaid

    def calculate_total_digidiscount(self):
        total_discount = sum(payment.digidiscount or 0 for payment in self.digipayments.all())
        return total_discount

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # ابتدا ذخیره‌سازی انجام می‌شود
        self.total_digiprice = self.calculate_total_digiprice()
        self.total_digipaid = self.calculate_total_digipaid()
        self.total_digidiscount = self.calculate_total_digidiscount()
        self.total_digiremain_amount = self.total_digiprice - self.total_digipaid
        super().save(*args, **kwargs)

# -------------------------------------------------------
class DigiProduct(models.Model):
    digiinvoice = models.ForeignKey(DigiInvoice, on_delete=models.CASCADE, related_name='digiitems', null=True,verbose_name='فاکتور')
    digicode = models.CharField(max_length=50, null=True, blank=True, verbose_name='کد کالا')
    diginame = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام کالا')
    qty = models.IntegerField(null=True, blank=True,verbose_name='تعداد')
    color = models.CharField(max_length=20, null=True, blank=True, verbose_name='رنگ کالا')
    brand = models.CharField(max_length=20, null=True, blank=True, verbose_name='برند کالا')
    model = models.CharField(max_length=20, null=True, blank=True, verbose_name='مدل')
    sale_tax = models.BigIntegerField( null=True, blank=True,verbose_name='مالیات فروش')
    unit_price = models.BigIntegerField(null=True, blank=True, verbose_name='قیمت واحد')
    digiprice = models.BigIntegerField(null=True, blank=True,verbose_name='قیمت فروش کالا')
    porsant_value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='پورسانت', default=0)

    def save(self, *args, **kwargs):
        if self.qty is not None and self.unit_price is not None:
            self.digiprice = self.qty * self.unit_price
        else:
            self.digiprice = 0
        super().save(*args, **kwargs)



    def __str__(self):
        return f" - {self.diginame} "

    class Meta:
        verbose_name = 'محصول دیجیتال'
        verbose_name_plural = 'محصولات دیجیتال'


# ----------------------------------------------------

class DigiPayment(models.Model):
    digiinvoice = models.ForeignKey(DigiInvoice, on_delete=models.CASCADE, related_name='digipayments', verbose_name='فاکتور دیجیتال')
    digiamount =models.PositiveIntegerField( verbose_name='مبلغ پرداخت')
    digidiscount = models.PositiveIntegerField(null=True, blank=True, verbose_name='تخفیف ')
    discount_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='کد تخفیف')  # فیلد کد تخفیف
    etebar = models.PositiveIntegerField(null=True, blank=True, verbose_name='مبلغ اعتبار ')
    etebar_code = models.CharField(max_length=20,null=True, blank=True, verbose_name='کد اعتبار')
    pay_date= jmodels.jDateField(verbose_name='تاریخ پرداخت', null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[('نقدی', 'نقدی'), ('اعتباری', 'اعتباری'),('تهاتر', 'تهاتر')], verbose_name='روش پرداخت')
    payment_explain = models.CharField(max_length=150, null=True, blank=True,verbose_name='شرح پرداخت')
    digipayment_receipt = models.CharField(max_length=50, null=True, blank=True, verbose_name='رسید پرداخت')
    digipayment_confirm = models.BooleanField(default=False, verbose_name='تایید پرداخت')

    def __str__(self):
        return f"پرداخت {self.digiamount}"

    class Meta:
        verbose_name = 'پرداخت دیجیتال'
        verbose_name_plural = 'پرداختهای دیجیتال'

# -------------------------------------------------------