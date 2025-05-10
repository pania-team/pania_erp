from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin, UserAdmin as BaseUserAdmin
from .models import User, Customer, Seller, HomeImage





# ======================= مدیریت کاربران ==========================
class UserAdmin(BaseUserAdmin):
    list_display = ('mellicod', 'phone', 'f_name', 'l_name')
    list_filter = ('is_active', 'groups')
    fieldsets = (
        ('User Info', {'fields': ('mellicod', 'password')}),
        ('Personal Info', {'fields': ('f_name', 'l_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'permission', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mellicod', 'f_name', 'l_name', 'phone', 'password1', 'password2', 'groups'),
        }),
    )
    search_fields = ('mellicod',)
    ordering = ('mellicod',)
    filter_horizontal = ('permission',)


# ======================= مدیریت مشتریان ==========================
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'mellicode', 'phone', 'phone_number', 'city')
    search_fields = ('first_name', 'last_name', 'mellicode')
    list_filter = ('city',)
    ordering = ('last_name', 'first_name')
    fieldsets = (
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'mellicode', 'phone', 'phone_number')}),
        ('اطلاعات مکانی', {'fields': ('city', 'code_posti', 'address')}),
    )


# ======================= مدیریت فروشندگان ==========================
@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller_porsant')
    search_fields = ('name',)


# ======================= مدیریت تصاویر صفحه اصلی ==========================
@admin.register(HomeImage)
class HomeImageAdmin(admin.ModelAdmin):
    list_display = ('id','description', 'image')

# ======================= ثبت مدل‌ها ==========================

admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
