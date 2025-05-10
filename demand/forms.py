
from django import forms
from .models import Loan
from .models import Repayment,Guarantee,Installment



# ======================================
#
class LoanForm(forms.ModelForm):
    class Meta:
            model = Loan
            fields = ['customer','plan', 'loan_date', 'start_date', 'end_date' ,'total_amount', 'final_amount', 'num_month', 'num_installments','loan_code']
            widgets = {
                'customer': forms.Select(
                    attrs={'class': 'form-control select2', 'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;', }),
                'plan': forms.Select(attrs={'class': 'form-control', 'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;', }),
                'loan_code': forms.TextInput(attrs={"placeholder": "کد وام","style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
                'total_amount': forms.NumberInput(attrs={'autocomplete': 'off',"placeholder": "مبلغ اعتبار" ,"style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
                'final_amount': forms.NumberInput(attrs={'autocomplete': 'off',"placeholder": "بازپرداخت نهایی" ,"style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
                'num_month': forms.NumberInput(
                    attrs={"placeholder": "تعداد قسط",'required': True , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
                'num_installments': forms.NumberInput(attrs={"placeholder": "تعداد بازپرداخت",'required': True ,
                                                             "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
                'loan_date': forms.TextInput(attrs={'data-jdp': 'true','class': 'form-control','required': True ,"placeholder":"تاریخ اخذ وام" ,"style": "font-family: Vazirmatn, sans-serif; font-size: 11px", 'autocomplete': 'off'}),
                'start_date': forms.TextInput(attrs={'data-jdp': 'true','class': 'form-control','required': True ,"placeholder":"تاریخ اولین قسط" ,"style": "font-family: Vazirmatn, sans-serif; font-size: 11px", 'autocomplete': 'off'}),
                'end_date': forms.TextInput(attrs={'data-jdp': 'true','class': 'form-control','required': True ,"placeholder":"تاریخ اخرین قسط" ,"style": "font-family: Vazirmatn, sans-serif; font-size: 11px", 'autocomplete': 'off'}),

            }
            labels = {
                'customer':'',
                'plan': 'طرح وام',
                'loan_code':'' ,
                'total_amount': '',
                'final_amount': '',
                'num_month': '',
                'num_installments': '',
                'loan_date': '',
                'start_date': '',
                'end_date': '',
            }
    def clean_loan_code(self):
        code = self.cleaned_data.get('loan_code')
        if not code:
            raise forms.ValidationError("کد وام تولید نشده است.")
        return code



# =====================================

class GuaranteeForm(forms.ModelForm):
    class Meta:
        model =Guarantee
        fields = [
             'guarantor_name', 'guarantee_amount', 'guarantee_serial','guarantee_type', 'guarantee_date',
            'guarantor_phone', 'guarantor_mellicod','guarantor_address']
        widgets = {
            'guarantor_name': forms.TextInput(attrs={"placeholder": "نام ضامن",'required': True, "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'guarantee_amount': forms.NumberInput(attrs={"placeholder": "مبلغ ضمانت", "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'guarantee_serial': forms.TextInput(attrs={"placeholder": "سریال تضامین", "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'guarantee_type': forms.Select(attrs={'required': True , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'guarantee_date': forms.TextInput(attrs={'data-jdp': 'true','class': 'form-control','required': True,"placeholder": "تاریخ ضمانت" , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px", 'autocomplete': 'off'}),
            'guarantor_phone': forms.TextInput(attrs={"placeholder": "شماره تماس ضامن" , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'guarantor_mellicod': forms.TextInput(attrs={"placeholder": "کد ملی ضامن" ,'required': True, "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'guarantor_address': forms.Textarea(attrs={"placeholder": "آدرس ضامن" , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
        }
        labels = {
            'guarantor_name': '',
            'guarantee_amount': '',
            'guarantee_serial': '',
            'guarantee_type': 'نوع ضمانت',
            'guarantee_date': '',
            'guarantor_phone': '',
            'guarantor_mellicod': '',
            'guarantor_address': '',
        }



class InstallmentForm(forms.ModelForm):
    class Meta:
        model = Installment
        fields = ['ghest_count', 'amount', 'due_date']



class RepaymentForm(forms.ModelForm):
    class Meta:
        model = Repayment
        fields = ['repayment_date','repayment_amount',  'payment_voucher', 'payment_method','payment_place']
        widgets = {
            'repayment_amount': forms.NumberInput(attrs={"placeholder": "مبلغ پرداخت", "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'repayment_date': forms.TextInput(attrs={'data-jdp': 'true','class': 'form-control','required': True,"placeholder": "تاریخ پرداخت" , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px", 'autocomplete': 'off'}),
            'payment_voucher': forms.TextInput(attrs={"placeholder": "رسید پرداخت" , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'payment_method': forms.Select(attrs={'required': True , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'payment_place': forms.Select(
                attrs={'required': True, "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
        }
        labels = {
            'repayment_amount': '',
            'repayment_date': '',
            'payment_voucher': '',
            'payment_method': '',
            'payment_place': '',
        }
# ------------------------------------------------



class UpdateInstallmentForm(forms.ModelForm):
    class Meta:
        model = Installment
        fields = ['ghest_type', 'ghest_place']
        widgets = {
            'ghest_type': forms.Select(attrs={'required': True, "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"}),
            'ghest_place': forms.TextInput(attrs={"placeholder": "محل پرداخت" , "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"})}
        labels = {
            'ghest_type': '',
            'ghest_place': '',
        }


