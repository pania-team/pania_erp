from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Repayment, Installment,Loan







# --------------------------------------

@receiver(post_save, sender=Repayment)
def update_installment_repaid_on_save(sender, instance, **kwargs):
    installment = instance.installment
    # محاسبه مجموع پرداختی‌ها
    total_repaid = installment.repayments.aggregate(Sum('repayment_amount'))['repayment_amount__sum'] or 0
    installment.total_ghest_repaid = total_repaid
    # به‌روزرسانی وضعیت پرداخت قسط
    if total_repaid >= installment.amount:
        installment.paid = True
    else:
        installment.paid = False
    installment.save()
    update_loan_mande_bedehi(installment.loan)

# ---------------------------------------------
@receiver(post_delete, sender=Repayment)
def update_installment_repaid_on_delete(sender, instance, **kwargs):
    installment = instance.installment
    total_repaid = installment.repayments.aggregate(Sum('repayment_amount'))['repayment_amount__sum'] or 0
    installment.total_ghest_repaid = total_repaid
    if total_repaid >= installment.amount:
        installment.paid = True
    else:
        installment.paid = False
    installment.save()
    update_loan_mande_bedehi(installment.loan)
# ----------------------------------------------


@receiver([post_save, post_delete], sender=Installment)
def update_total_received_customer(sender, instance, **kwargs):
    loan = instance.loan
    total_received_customer = Installment.objects.filter(loan=loan).aggregate(
        Sum('total_ghest_repaid')
    )['total_ghest_repaid__sum'] or 0
    loan.total_received_customer = total_received_customer
    loan.save()
    update_loan_mande_bedehi(loan)
# ----------------------------------------

def update_loan_mande_bedehi(loan):
    try:
        total_repayments = loan.installments.aggregate(
            total=Sum('total_ghest_repaid')
        )['total'] or 0
        loan.total_received_customer = total_repayments
        loan.loan_mande_bedehi = max(0, loan.final_amount - total_repayments)
        loan.save()
    except AttributeError:
        print("خطا در دسترسی به وام مرتبط.")