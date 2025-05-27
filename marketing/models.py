from django.db import models
import django_jalali.db.models as jmodels




# ------------------------------------
class Product(models.Model):
    TYPE_CHOICES = [
        ('mobile', 'موبایل'),
        ('laptop', 'لپ‌تاپ'),
        ('watch', 'طلا'),
        ('other', 'سایر'),
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="نوع کالا")
    brand = models.CharField(max_length=100, verbose_name="برند")
    model_name = models.CharField(max_length=100, verbose_name="مدل کالا")

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.get_type_display()})"
# --------------------------------------------------------
class Lead(models.Model):
    SOURCE_CHOICES = [
        ('instagram', 'اینستاگرام'),
        ('website', 'وب‌سایت'),
        ('referral', 'معرفی'),
        ('whatsapp', 'واتساپ'),
        ('other', 'سایر'),
    ]
    requested_products = models.ManyToManyField(Product, blank=True, verbose_name="کالاهای درخواستی")
    first_name = models.CharField(max_length=50, verbose_name='نام', null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی', null=True, blank=True)
    mellicode = models.CharField(max_length=15, blank=True, null=True, verbose_name='کد ملی')
    phone = models.CharField(max_length=11, verbose_name='شماره ثابت', null=True, blank=True)
    phone_number = models.CharField(max_length=11, verbose_name='تلفن همراه', null=False, blank=False)
    source = models.CharField(max_length=50,choices=SOURCE_CHOICES, blank=True,null=True,verbose_name="منبع")
    city = models.CharField(max_length=50, verbose_name='شهر', null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.last_name

# -------------------------------
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# ------------------------------------------
class FollowUp(models.Model):
    FOLLOW_TYPE_CHOICES = [
        ('call', 'تماس تلفنی'),
        ('sms', 'پیامک'),
        ('whatsapp', 'واتساپ'),
        ('in_person', 'حضوری'),
        ('other', 'سایر'),
    ]
    lead = models.ForeignKey('Lead', on_delete=models.CASCADE, verbose_name="لید")
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="پیگیری‌کننده")
    follow_date = jmodels.jDateTimeField(verbose_name="تاریخ پیگیری")
    follow_type = models.CharField(max_length=20, choices=FOLLOW_TYPE_CHOICES, verbose_name="نوع پیگیری")
    subject = models.CharField(max_length=100, blank=True, verbose_name="موضوع پیگیری")
    notes = models.TextField(blank=True, verbose_name="یادداشت‌ها")
    follow_up_required = models.BooleanField(default=False, verbose_name="نیاز به پیگیری مجدد")
    next_followup_date = jmodels.jDateTimeField(null=True, blank=True, verbose_name="تاریخ پیگیری بعدی")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-follow_date']
        verbose_name = "پیگیری"
        verbose_name_plural = "پیگیری‌ها"

    def __str__(self):
        return f"{self.lead} - {self.follow_date.strftime('%Y-%m-%d')} - {self.follow_type}"

# -----------------------------------------------