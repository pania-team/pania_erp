from django.db import models
from django_jalali.db import models as jmodels
from django.utils import timezone






class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='نام دسته')
    description = models.TextField(blank=True, verbose_name='شرح')

    def __str__(self):
        return self.name


# -----------------------------------
# اطلاعات عمومی کالا
class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام کالا')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    sku = models.CharField(max_length=50, unique=True, verbose_name='شناسه کالا')  # شناسه یکتا
    brand = models.CharField(max_length=100, blank=True, verbose_name='برند')
    image = models.ImageField(upload_to='item_images/', blank=True, null=True, verbose_name='تصویر')
    created_at = jmodels.jDateTimeField(default=timezone.now)
    description = models.TextField(blank=True, verbose_name='شرح')
    buy_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='مبلغ خرید')
    buy_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='مالیات خرید')
    def __str__(self):
        return f"{self.name} ({self.sku}) - {self.category.name}"


# ----------------------------------
# ویژگی های اختصاصی کالا

class ItemAttribute(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='attributes', verbose_name='کالا')
    key = models.CharField(max_length=100, verbose_name='ویژگی')  # مثلاً: رنگ، وزن، حجم
    value = models.CharField(max_length=200, verbose_name='مقدار')  # مثلاً: آبی، 5 کیلوگرم

    class Meta:
        unique_together = ('item', 'key')
        verbose_name = 'ویژگی کالا'
        verbose_name_plural = 'ویژگی‌های کالا'

    def __str__(self):
        return f"{self.item.name} | {self.key}: {self.value}"


# -------------------------------------------
# موجودی و محل نگهداری
class Inventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20, default='عدد', verbose_name='واحد')  # یا کیلوگرم، متر و غیره
    location = models.CharField(max_length=100, blank=True, verbose_name='محل انبار')  # قفسه، انبار، منطقه
    last_updated = jmodels.jDateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('available', 'موجود'),
        ('reserved', 'رزرو شده'),
        ('damaged', 'آسیب‌دیده'),
        ('out', 'خارج شده')
    ], default='available')



    def __str__(self):
        return f"{self.item.name} - {self.quantity} {self.unit} @ {self.location}"

# --------------------------------------------------