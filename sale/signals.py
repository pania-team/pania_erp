from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GoldProduct,GoldPayment,DigiInvoice,DigiPayment



@receiver(post_save, sender=GoldPayment)
def update_gold_invoice_status(sender, instance, **kwargs):
    invoice = instance.goldinvoice
    has_unconfirmed_payments = invoice.payments.filter(payment_confirm=False).exists()
    if not has_unconfirmed_payments:
        invoice.status = 'paid'
        invoice.save()






@receiver(post_save, sender=GoldPayment)
def update_invoice_status(sender, instance, **kwargs):
    invoice = instance.goldinvoice
    has_unconfirmed_payments = invoice.payments.filter(payment_confirm=False).exists()
    if not has_unconfirmed_payments:
        # اگر هیچ پرداخت تأیید نشده‌ای وجود ندارد، وضعیت فاکتور را به 'paid' تغییر دهید
        invoice.status = 'paid'
        invoice.save()
