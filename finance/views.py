from django.shortcuts import render, redirect, get_object_or_404
from sale.models import GoldPayment,DigiPayment
from .forms import GoldPaymentConfirmForm,DigiPaymentConfirmForm
from accounts.models import Customer
# ---------------------------------
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from jdatetime import datetime as jdatetime
import jdatetime










@login_required
def list_payments(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    seller = request.GET.get('seller')
    customer_name = request.GET.get('customer')  # نام و نام خانوادگی مشتری
    payments = GoldPayment.objects.filter(payment_confirm=False)
    start_date_jalali = ''
    end_date_jalali = ''
    has_filter = bool(start_date or end_date or customer_name or seller)
    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()
        payments = payments.filter(pay_date__range=(start_date_gregorian, end_date_gregorian))
        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y-%m-%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y-%m-%d')

    if seller:
        payments = payments.filter(goldinvoice__seller__name__icontains=seller)

    if customer_name:
        if ' ' in customer_name:
            first_name, last_name = customer_name.split(' ', 1)
            payments = payments.filter(
                Q(goldinvoice__customersale__first_name__icontains=first_name) &
                Q(goldinvoice__customersale__last_name__icontains=last_name)
            )
        else:
            payments = payments.filter(
                Q(goldinvoice__customersale__first_name__icontains=customer_name) |
                Q(goldinvoice__customersale__last_name__icontains=customer_name)
            )
    if has_filter:
        payments = payments.order_by('pay_date')
    else:
        payments = payments.order_by('-pay_date')
    context = {
        'payments': payments,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'customer_name': customer_name,
        'seller': seller,
    }
    return render(request, 'finance/list_payments.html', context)


# ------------------------------------------------

@login_required
def add_goldpayment_reciept(request, payments_id):
    payment = get_object_or_404(GoldPayment, id=payments_id)
    if request.method == 'POST':
        form = GoldPaymentConfirmForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات پرداخت با موفقیت ثبت شد.')
            return redirect('finance:list_payments') 
    else:
        form = GoldPaymentConfirmForm(instance=payment)
    return render(request, 'finance/add_goldpayment_reciept.html', {
        'payment': payment,
        'form': form,
    })

# ---------------------------------------------------------
@login_required
def list_appro_payments(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    seller = request.GET.get('seller')
    customer_name = request.GET.get('customer')
    payments = GoldPayment.objects.filter(payment_confirm=True)
    start_date_jalali = ''
    end_date_jalali = ''
    has_filter = bool(start_date or end_date or customer_name or seller)
    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()
        payments = payments.filter(pay_date__range=(start_date_gregorian, end_date_gregorian))
        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y-%m-%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y-%m-%d')

    if seller:
        payments = payments.filter(goldinvoice__seller__name__icontains=seller)

    if customer_name:
        if ' ' in customer_name:
            first_name, last_name = customer_name.split(' ', 1)
            payments = payments.filter(
                Q(goldinvoice__customersale__first_name__icontains=first_name) &
                Q(goldinvoice__customersale__last_name__icontains=last_name)
            )
        else:
            payments = payments.filter(
                Q(goldinvoice__customersale__first_name__icontains=customer_name) |
                Q(goldinvoice__customersale__last_name__icontains=customer_name)
            )
    if has_filter:
        payments = payments.order_by('pay_date')
    else:
        payments = payments.order_by('-pay_date')[:12]
    context = {
        'payments': payments,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'customer_name': customer_name,
        'seller': seller,
    }
    return render(request, 'finance/list_appro_payments.html', context)

# =======================DIGI ================


@login_required
def list_digipayments(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    seller = request.GET.get('seller')
    customer_name = request.GET.get('customer')
    payments = DigiPayment.objects.filter(digipayment_confirm=False)
    start_date_jalali = ''
    end_date_jalali = ''
    has_filter = bool(start_date or end_date or customer_name or seller)
    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()
        payments = payments.filter(pay_date__range=(start_date_gregorian, end_date_gregorian))
        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y-%m-%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y-%m-%d')

    if seller:
        payments = payments.filter(digiinvoice__seller__name__icontains=seller)

    if customer_name:
        if ' ' in customer_name:
            first_name, last_name = customer_name.split(' ', 1)
            payments = payments.filter(
                Q(digiinvoice__customersale__first_name__icontains=first_name) &
                Q(digiinvoice__customersale__last_name__icontains=last_name)
            )
        else:
            payments = payments.filter(
                Q(digiinvoice__customersale__first_name__icontains=customer_name) |
                Q(digiinvoice__customersale__last_name__icontains=customer_name)
            )
    if has_filter:
        payments = payments.order_by('pay_date')
    else:
        payments = payments.order_by('-pay_date')
    context = {
        'payments': payments,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'customer_name': customer_name,
        'seller': seller,
    }
    return render(request, 'finance/list_digipayments.html', context)
# ------------------------------------------------


@login_required
def add_digipayment_reciept(request, payments_id):
    payment = get_object_or_404(DigiPayment, id=payments_id)
    if request.method == 'POST':
        form = DigiPaymentConfirmForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات پرداخت با موفقیت ثبت شد.')
            return redirect('finance:list_digipayments')
    else:
        form = DigiPaymentConfirmForm(instance=payment)
    return render(request, 'finance/add_digipayment_reciept.html', {
        'payment': payment,
        'form': form,
    })
# ---------------------------------

@login_required
def list_appro_digipayments(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    seller = request.GET.get('seller')
    customer_name = request.GET.get('customer')
    payments = DigiPayment.objects.filter(digipayment_confirm=True)
    start_date_jalali = ''
    end_date_jalali = ''
    has_filter = bool(start_date or end_date or customer_name or seller)
    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()
        payments = payments.filter(pay_date__range=(start_date_gregorian, end_date_gregorian))
        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y-%m-%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y-%m-%d')

    if seller:
        payments = payments.filter(digiinvoice__seller__name__icontains=seller)

    if customer_name:
        if ' ' in customer_name:
            first_name, last_name = customer_name.split(' ', 1)
            payments = payments.filter(
                Q(digiinvoice__customersale__first_name__icontains=first_name) &
                Q(digiinvoice__customersale__last_name__icontains=last_name)
            )
        else:
            payments = payments.filter(
                Q(digiinvoice__customersale__first_name__icontains=customer_name) |
                Q(digiinvoice__customersale__last_name__icontains=customer_name)
            )
    if has_filter:
        payments = payments.order_by('pay_date')
    else:
        payments = payments.order_by('-pay_date')[:12]
    context = {
        'payments': payments,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'customer_name': customer_name,
        'seller': seller,
    }
    return render(request, 'finance/list_appro_digipayments.html', context)
