from django import forms
from .models import User,Customer
import re




# --------------------------------------------
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['mellicode','first_name', 'last_name',  'phone_number', 'city', 'address']
        widgets = {
            'mellicode': forms.TextInput(attrs={"placeholder": "کد ملی", 'required': True,
                                                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px", 'autocomplete': 'off'}),
            'first_name': forms.TextInput(attrs={"placeholder": "نام", 'required': True,
                                                 "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'last_name': forms.TextInput(
                attrs={"placeholder": "نام خانوادگی", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),

            'phone_number': forms.TextInput(
                attrs={"placeholder": "شماره همراه", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px", 'autocomplete': 'off'}),
            'city': forms.TextInput(
                attrs={"placeholder": "شهر", "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
            'address': forms.Textarea(attrs={"placeholder": "آدرس", 'required': True,
                                             "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"}),
        }
        labels = {
            'mellicode': '',
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'city': '',
            'address': '',
        }


    # بررسی صحت کدملی
    def clean_mellicode(self):
        mellicode = self.cleaned_data['mellicode']
        if len(mellicode) != 10 or not mellicode.isdigit():
            raise forms.ValidationError("کد ملی باید شامل ۱۰ رقم باشد.")

        digits = [int(digit) for digit in mellicode]
        checksum = sum(digits[i] * (10 - i) for i in range(9))
        rem = checksum % 11

        if rem < 2:
            if digits[9] != rem:
                raise forms.ValidationError("کد ملی وارد شده معتبر نیست")
        else:
            if digits[9] != (11 - rem):
                raise forms.ValidationError("کد ملی وارد شده معتبر نیست")
        return mellicode


    # بررسی صحت موبایل
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        mobile_regex = r"^09\d{9}$"
        if not re.match(mobile_regex, phone_number):
                raise forms.ValidationError("شماره تلفن همراه معتبر نیست.")
        return phone_number

