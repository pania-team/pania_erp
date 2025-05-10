from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from .models import Customer
from demand.models import Loan



@receiver([post_save, post_delete], sender=Loan)
def update_customer_loan_summary(sender, instance, **kwargs):
    customer = instance.customer

    total_loan_amount = customer.loans.aggregate(
        total_amount_sum=Sum('total_amount')
    )['total_amount_sum'] or 0

    total_loan_balance = customer.loans.aggregate(
        loan_mande_bedehi_sum=Sum('loan_mande_bedehi')
    )['loan_mande_bedehi_sum'] or 0

    total_repaid = customer.loans.aggregate(
        total_received_customer_sum=Sum('total_received_customer')
    )['total_received_customer_sum'] or 0

    customer.total_loan_amount = total_loan_amount
    customer.total_loan_balance = total_loan_balance
    customer.total_repaid = total_repaid

    print(f"Updating customer {customer.id}: {total_loan_amount=}, {total_loan_balance=}, {total_repaid=}")

    customer.save()
