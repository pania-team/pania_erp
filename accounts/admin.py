from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as DefaultGroupAdmin, UserAdmin as BaseUserAdmin
from .models import User, Customer, Seller, HomeImage
from django import forms




# ======================= مدیریت کاربران ==========================


class UserAdmin(BaseUserAdmin):

    list_display = ('l_name', 'f_name','mellicod', 'get_groups', 'superuser_status','admin_status', 'active_status','role', 'get_manager_chain')
    list_filter = ('is_active', 'groups', 'role')
    fieldsets = (
        ('User Info', {'fields': ('mellicod', 'password')}),
        ('Personal Info', {'fields': ('f_name', 'l_name', 'phone','role', 'manager')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'user_permissions', 'groups')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mellicod', 'f_name', 'l_name', 'phone', 'role', 'manager',
                       'password1', 'password2', 'is_active', 'is_admin', 'is_superuser', 'user_permissions', 'groups'),
        }),
    )

    search_fields = ('l_name', 'f_name',)
    ordering = ('mellicod',)
    filter_horizontal = ('user_permissions', 'groups')


    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Groups'

    @admin.display(boolean=True, description='Active')
    def active_status(self, obj):
        return obj.is_active

    @admin.display(boolean=True, description='Admin')
    def admin_status(self, obj):
        return obj.is_admin

    @admin.display(boolean=True, description='Superuser')
    def superuser_status(self, obj):
        return obj.is_superuser


    def get_manager_chain(self, obj):
        managers = []
        current = obj.manager
        while current:
            managers.append(f"{current.l_name}")
            current = current.manager
        return "←".join(managers) if managers else "-"
    get_manager_chain.short_description = 'زنجیره مدیران مافوق'


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
