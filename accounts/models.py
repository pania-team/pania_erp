
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Permission
from django.db import models
from django.core.exceptions import ValidationError
import re



# =================================کاربران نرم افزار====================
class UserManager(BaseUserManager):
    def create_user(self, mellicod, f_name, l_name, phone, password=None):
        if not mellicod:
            raise ValueError('کاربر باید کد ملی داشته باشد')
        user = self.model(mellicod=mellicod, f_name=f_name, l_name=l_name, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mellicod, f_name, l_name, phone, password=None):
        user = self.create_user(mellicod, f_name, l_name, phone, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('EMPLOYEE', 'کارمند'),
        ('SUPERVISOR', 'سرپرست'),
        ('MANAGER', 'مدیر'),
        ('CEO', 'مدیرعامل'),
    ]
    f_name = models.CharField(max_length=50, verbose_name='نام', blank=True, null=True)
    l_name = models.CharField(max_length=50, verbose_name='فامیلی', blank=True, null=True)
    mellicod = models.CharField(max_length=15, verbose_name='کدملی', unique=True)
    phone = models.CharField(max_length=15, verbose_name='موبایل', blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ', blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='EMPLOYEE', verbose_name='جایگاه')
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='team_members',
                                verbose_name='مدیر مافوق', help_text="مدیر مافوق کاربر")

    is_superuser = models.BooleanField(default=False, verbose_name='Superuser ')
    is_admin = models.BooleanField(default=False, verbose_name='دسترسی به پنل ادمین')
    is_active = models.BooleanField(default=True, verbose_name='کاربر فعال')


    USERNAME_FIELD = 'mellicod'
    REQUIRED_FIELDS = ['phone', 'f_name', 'l_name']
    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return f"{self.l_name} {self.f_name} "

        # شرط دسترسی به پنل ادمین
    @property
    def is_staff(self):
        return self.is_admin or self.is_superuser

            # تمام کاربران زیرمجموعه این کاربر را برمی‌گرداند.
    def get_all_subordinates(self):
        subordinates = list(self.team_members.all())
        for member in self.team_members.all():
            subordinates += member.get_all_subordinates()
        return subordinates

# ============================ مشتریان  =====================

class Customer(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='نام', null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی', null=True, blank=True)
    mellicode = models.CharField(max_length=10,unique=True ,verbose_name='کد ملی')
    phone = models.CharField(max_length=11, verbose_name='شماره ثابت', null=True, blank=True)
    phone_number = models.CharField(max_length=11, verbose_name='تلفن همراه', null=True, blank=True)
    city= models.CharField(max_length=50,verbose_name='شهر', null=True, blank=True)
    code_posti = models.CharField(max_length=255, verbose_name='کدپستی', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='آدرس', null=True, blank=True)
    total_loan_amount = models.BigIntegerField(default=0, verbose_name='مجموع وام‌های دریافتی')
    total_loan_balance = models.BigIntegerField(default=0, verbose_name='مانده کل وام‌ها')
    total_repaid = models.BigIntegerField(default=0, verbose_name='مجموع پرداختی مشتری')

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"

    def __str__(self):
        return f'{self.first_name} {self.last_name} '


# ==========================================
class HomeImage(models.Model):
    image = models.ImageField(upload_to='home_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or "Image"

# ====================================
class Seller(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام')
    seller_porsant=models.DecimalField(max_digits=5, decimal_places=2, verbose_name='پورسانت فروشنده', default=0)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "فروشنده"
        verbose_name_plural = "فروشندگان"

# ============================   -مدل تامین کنندگان   -===========================


class Supplier(models.Model):
    SUPPLIER_TYPE_CHOICES = (
        ('individual', 'شخص حقیقی'),
        ('company', 'شرکت '),
    )
    type = models.CharField(
        max_length=10,
        choices=SUPPLIER_TYPE_CHOICES,
        default='individual',
        verbose_name='نوع تأمین‌کننده'
    )
    # برای شخص حقیقی
    first_name = models.CharField(max_length=50, verbose_name='نام', null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی', null=True, blank=True)
    mellicode = models.CharField(max_length=15, blank=True, null=True, verbose_name='کد ملی')
    # برای شرکت
    company_name = models.CharField(max_length=100, verbose_name='نام شرکت', null=True, blank=True)
    company_code = models.CharField(max_length=20, verbose_name='شناسه ملی / ثبت شرکت', null=True, blank=True)
    # اطلاعات تماس مشترک
    phone = models.CharField(max_length=11, verbose_name='شماره ثابت', null=True, blank=True)
    phone_number = models.CharField(max_length=11, verbose_name='تلفن همراه', null=False, blank=False)
    city = models.CharField(max_length=50, verbose_name='شهر', null=True, blank=True)
    code_posti = models.CharField(max_length=15, verbose_name='کدپستی', null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name='آدرس', null=True, blank=True)

    class Meta:
        verbose_name = "تأمین‌کننده"
        verbose_name_plural = "تأمین‌کنندگان"

    def __str__(self):
        if self.type == 'individual':
            return f'{self.first_name or ""} {self.last_name or ""}'.strip()
        elif self.type == 'company':
            return self.company_name or "شرکت بدون‌نام"
        return "تأمین‌کننده"

    def clean(self):
        # اعتبارسنجی شماره موبایل
        if self.phone_number:
            mobile_regex = r"^09\d{9}$"
            if not re.match(mobile_regex, self.phone_number):
                raise ValidationError("شماره تلفن همراه را به‌درستی وارد کنید.")

        # بررسی پر بودن فیلدهای متناسب با نوع
        if self.type == 'individual':
            if not self.first_name or not self.last_name:
                raise ValidationError("برای شخص حقیقی، نام و نام خانوادگی الزامی است.")
        elif self.type == 'company':
            if not self.company_name:
                raise ValidationError("برای شرکت، وارد کردن نام شرکت الزامی است.")

# -----------------------------------------------