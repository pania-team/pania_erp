from django.contrib import admin
from accounts.models import Supplier
from .models import Category, Item, ItemAttribute, Inventory,BuyInvoice




# --------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


# --------------------------
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'brand', 'formatted_base_price', 'formatted_base_tax', 'created_at')
    search_fields = ('name', 'sku', 'brand')
    list_filter = ('category', 'created_at')
    date_hierarchy = 'created_at'

    def formatted_base_price(self, obj):
        return f"{obj.base_price:,}"
    formatted_base_price.short_description = 'مبلغ پایه'

    def formatted_base_tax(self, obj):
        return f"{obj.base_tax:,}"
    formatted_base_tax.short_description = 'مالیات پایه'


# --------------------------
@admin.register(ItemAttribute)
class ItemAttributeAdmin(admin.ModelAdmin):
    list_display = ('item', 'key', 'value')
    search_fields = ('item__name', 'key', 'value')


# --------------------------
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'unit', 'location', 'status', 'last_updated')
    search_fields = ('item__name', 'location')
    list_filter = ('status', 'last_updated')
    date_hierarchy = 'last_updated'

# --------------------------------------------


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'type', 'phone_number', 'phone', 'city', 'code_posti', 'address')
    list_filter = ('type', 'city')
    search_fields = ('first_name', 'last_name', 'company_name', 'mellicode', 'company_code', 'phone_number')
    ordering = ('type', 'last_name', 'company_name')

    def display_name(self, obj):
        if obj.type == 'individual':
            return f"{obj.first_name or ''} {obj.last_name or ''}".strip()
        elif obj.type == 'company':
            return obj.company_name or "شرکت بدون‌نام"
        return "نام نامشخص"
    display_name.short_description = 'نام تأمین‌کننده'

# ---------------------------------------------

@admin.register(BuyInvoice)
class BuyInvoiceAdmin(admin.ModelAdmin):
    list_display = ( 'date', 'supplier', 'formatted_total_amount', 'formatted_discount_amount')
    search_fields = ('supplier__first_name', 'supplier__last_name', )
    list_filter = ( 'date',)
    date_hierarchy = 'date'

    def formatted_total_amount(self, obj):
        return f"{obj.total_amount:,}"  # نمایش قیمت بصورت سه تایی اعداد
    formatted_total_amount.short_description = 'جمع مبلغ فاکتور'


    def formatted_discount_amount(self, obj):
        return f"{obj.discount_amount:,}"  # نمایش قیمت بصورت سه تایی اعداد
    formatted_discount_amount.short_description = 'جمع تخفیف'

# ----------------------------------------

from django.contrib import admin
from .models import BuyItem

@admin.register(BuyItem)
class BuyItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'invoice', 'quantity', 'unit_price', 'tax', 'discount_kala')
    list_filter = ('invoice', 'item')
    search_fields = ('item__name', 'invoice__id')
