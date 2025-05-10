from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse

from .forms import GoldInvoiceForm, GoldPaymentForm, GoldProductForm
from .forms import DigiInvoiceForm, DigiPaymentForm, DigiProductForm
from .models import Seller, GoldInvoice, GoldPayment, GoldProduct
from .models import DigiInvoice, DigiPayment, DigiProduct

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.db.models import Q

import arabic_reshaper
from bidi.algorithm import get_display
# from django.utils.dateparse import parse_date

from datetime import datetime
import jdatetime
from jdatetime import datetime as jdatetime





@login_required
def create_goldinvoice(request):
    if request.method == 'POST':
        invoice_form = GoldInvoiceForm(request.POST)
        jalali_date = invoice_form.data['date']  # دریافت تاریخ جلالی از فرم
        try:
            formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            invoice_form.data = invoice_form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
            invoice_form.data['date'] = formatted_date
        except ValueError:
            invoice_form.add_error('date', 'تاریخ وارد شده نامعتبر است.')
        if invoice_form.is_valid():
            invoice_form.save()  # ذخیره فرم
            return redirect('sale:goldsale_list')  # هدایت به لیست فاکتورها
    else:
        invoice_form = GoldInvoiceForm()

    return render(request, 'sale/create_goldinvoice.html', {
        'invoice_form': invoice_form,
    })



# ===========================================

@login_required
def add_goldinvoice_items(request, goldinvoice_id):
    invoice = get_object_or_404(GoldInvoice, id=goldinvoice_id)  # دریافت فاکتور
    if request.method == 'POST':
        goldproduct_form = GoldProductForm(request.POST)
        if goldproduct_form.is_valid():
            gold_product = goldproduct_form.save(commit=False)
            gold_product.goldinvoice = invoice  # ارتباط محصول با فاکتور
            gold_product.save()  # اینجا شیء جدید به پایگاه داده ذخیره می‌شود
            goldproduct_form = GoldProductForm()  # فرم جدید برای خالی شدن
    else:
        goldproduct_form = GoldProductForm()
    return render(request, 'sale/add_goldinvoice_items.html', {
        'invoice': invoice,
        'goldproduct_form': goldproduct_form,
    })


# ===================================

@login_required
def add_goldpayment(request, goldinvoice_id):
    invoice = get_object_or_404(GoldInvoice, id=goldinvoice_id)  # دریافت فاکتور
    if request.method == 'POST':
        payment_form = GoldPaymentForm(request.POST)
        jalali_date = payment_form.data['pay_date']
        try:
            formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            payment_form.data = payment_form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
            payment_form.data['pay_date'] = formatted_date
        except ValueError:
            payment_form.add_error('pay_date', 'تاریخ وارد شده نامعتبر است.')
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)  # نجات داده بدون ذخیره
            payment.goldinvoice = invoice  # ارتباط با فاکتور
            payment.save()  # ذخیره پرداخت
            # بازگردانی به همان صفحه برای اضافه کردن پرداخت‌های جدید
            return redirect('sale:add_goldpayment', goldinvoice_id=invoice.id)
    else:
        payment_form = GoldPaymentForm()
    return render(request, 'sale/add_goldpayment.html', {
        'payment_form': payment_form,
        'invoice': invoice,
    })

# ===================================================

from django.db.models import Sum, F, Prefetch
import jdatetime

@login_required
def goldsale_list(request):
    if request.GET:
        request.session['goldsale_list_filters'] = {
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
            'seller': request.GET.get('seller', ''),
            'customer': request.GET.get('customer', ''),
        }

    filters = request.session.get('goldsale_list_filters', {})
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')
    seller = filters.get('seller', '')
    customer_name = filters.get('customer', '')
    gold_sales = GoldInvoice.objects.all()
    start_date_jalali = ''
    end_date_jalali = ''

    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))

        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()

        gold_sales = gold_sales.filter(date__range=(start_date_gregorian, end_date_gregorian))

        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y/%m/%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y/%m/%d')

    if seller:
        gold_sales = gold_sales.filter(seller__name__icontains=seller)

    if customer_name:
        gold_sales = gold_sales.filter(
            Q(customersale__last_name__icontains=customer_name) |
            Q(customersale__first_name__icontains=customer_name)
        )

    gold_sales = gold_sales.prefetch_related(
        Prefetch('payments'),
        Prefetch('golditems')
    ).order_by('-date')

    if not (start_date or end_date or seller or customer_name):
        gold_sales = gold_sales[:10]

    invoice_data = []
    all_paid = 0
    all_amount = 0
    all_weight = 0
    all_discount = 0
    all_calcu_amount = 0
    all_remain_amount = 0

    for invoice in gold_sales:
        total_paid = invoice.payments.aggregate(total_paid=Sum('amount'))['total_paid'] or 0
        total_discount = invoice.payments.aggregate(total_discount=Sum('discount'))['total_discount'] or 0
        total_amount = invoice.golditems.aggregate(total_amount=Sum('price'))['total_amount'] or 0
        total_weight = invoice.golditems.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        total_calcu_amount = invoice.golditems.aggregate(total_calcu_amount=Sum('calcu_amount'))['total_calcu_amount'] or 0
        total_remain_amount = total_amount - total_paid - total_discount
        kalanum = invoice.golditems.count()
        invoice.total_paid = total_paid
        invoice.total_discount = total_discount
        invoice.total_amount = total_amount
        invoice.total_weight = total_weight
        invoice.total_calcu_amount = total_calcu_amount
        invoice.total_remain_amount = total_remain_amount
        invoice.save()
        invoice_data.append({
            'invoice': invoice,
            'kalanum': kalanum,
        })
        all_paid += total_paid
        all_amount += total_amount
        all_weight += total_weight
        all_discount += total_discount
        all_calcu_amount += total_calcu_amount
        all_remain_amount += total_remain_amount

    context = {
        'gold_sales': gold_sales,
        'all_weight': all_weight,
        'all_paid': all_paid,
        'all_amount': all_amount,
        'all_discount': all_discount,
        'all_calcu_amount': all_calcu_amount,
        'all_remain_amount': all_remain_amount,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'seller': seller,
        'customer_name': customer_name,
        'invoice_data': invoice_data,
        'filters': filters,
    }
    return render(request, 'sale/goldsale_list.html', context)

# ================================================

@login_required
def goldsale_detail(request, goldinvoice_id):
    invoice = get_object_or_404(GoldInvoice, pk=goldinvoice_id)
    items = invoice.golditems.all()
    payments = invoice.payments.all()
    for item in items:
        sale_benefit = item.calculate_weighted_benefit()
        item.sale_benefit = sale_benefit
    total_weight = sum(item.weight or 0 for item in items)
    total_discount = sum(payment.discount or 0 for payment in payments)
    total_amount = sum(item.price or 0 for item in items)
    total_paid = sum(payment.amount for payment in payments)
    remaining_amount = total_amount - total_paid - total_discount
    context = {
        'invoice': invoice,
        'items': items,
        'payments': payments,
        'total_weight':total_weight,
        'total_paid':total_paid,
        'total_amount':total_amount,
        'total_discount':total_discount,
        'remaining_amount': remaining_amount,
    }
    return render(request, 'sale/goldsale_detail.html', context)

# ======================== DIGITAL=========================

# ایجاد فاکتور
@login_required
def create_digiinvoice(request):
    if request.method == 'POST':
        form = DigiInvoiceForm(request.POST)
        jalali_date = form.data['date']  # دریافت تاریخ جلالی از فرم
        try:
            formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            form.data = form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
            form.data['date'] = formatted_date
        except ValueError:
            form.add_error('date', 'تاریخ وارد شده نامعتبر است.')
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.save()
            return redirect('sale:digisale_list')  # هدایت به لیست فاکتورها
    else:
        form = DigiInvoiceForm()
    return render(request, 'sale/create_digiinvoice.html', {'form': form})

# ----------------------------------------------------------
import jdatetime


@login_required
def digisale_list(request):
    if request.GET:
        request.session['digisale_list_filters'] = {
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
            'seller': request.GET.get('seller', ''),
            'customer': request.GET.get('customer', ''),
        }

    filters = request.session.get('digisale_list_filters', {})
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')
    seller = filters.get('seller', '')
    customer_name = filters.get('customer', '')
    digi_sales = DigiInvoice.objects.all()
    start_date_jalali = ''
    end_date_jalali = ''
    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))

        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()

        digi_sales = digi_sales.filter(date__range=(start_date_gregorian, end_date_gregorian))

        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y/%m/%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y/%m/%d')

    if seller:
        digi_sales = digi_sales.filter(seller__name__icontains=seller)

    if customer_name:
        digi_sales = digi_sales.filter(
            Q(customersale__last_name__icontains=customer_name) |
            Q(customersale__first_name__icontains=customer_name)
        )

    digi_sales = digi_sales.prefetch_related(
        Prefetch('digipayments'),
        Prefetch('digiitems')
    ).order_by('-date')

    # محدود کردن به 10 رکورد آخر در صورت عدم وجود فیلتر
    if not (start_date or end_date or seller or customer_name):
        digi_sales = digi_sales[:10]
    invoice_data = []
    all_paid = 0
    all_amount = 0
    all_discount = 0
    all_remain_amount = 0
    for invoice in digi_sales:
        total_paid = invoice.digipayments.aggregate(total_paid=Sum('digiamount'))['total_paid'] or 0
        total_discount = invoice.digipayments.aggregate(total_discount=Sum('digidiscount'))['total_discount'] or 0
        total_amount = invoice.digiitems.aggregate(total_amount=Sum('digiprice'))['total_amount'] or 0
        total_remain_amount = total_amount - total_paid - total_discount
        kalanum = invoice.digiitems.count()
        invoice.total_paid = total_paid
        invoice.total_discount = total_discount
        invoice.total_amount = total_amount
        invoice.total_remain_amount = total_remain_amount
        invoice.save()
        invoice_data.append({
            'invoice': invoice,
            'kalanum': kalanum,
        })
        all_paid += total_paid
        all_amount += total_amount
        all_discount += total_discount
        all_remain_amount += total_remain_amount

    context = {
        'digi_sales': digi_sales,
        'all_paid': all_paid,
        'all_amount': all_amount,
        'all_discount': all_discount,
        'all_remain_amount': all_remain_amount,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'seller': seller,
        'customer_name': customer_name,
        'invoice_data': invoice_data,
        'filters': filters,
    }
    return render(request, 'sale/digisale_list.html', context)

# ---------------------------------------------------------------

@login_required
def add_digiinvoice_items(request, digiinvoice_id):
    invoice = get_object_or_404(DigiInvoice, id=digiinvoice_id)
    if request.method == 'POST':
        digiproduct_form = DigiProductForm(request.POST)
        if digiproduct_form.is_valid():
            digi_product = digiproduct_form.save(commit=False)
            digi_product.digiinvoice = invoice  # ارتباط محصول با فاکتور
            digi_product.save()  # اینجا شیء جدید به پایگاه داده ذخیره می‌شود
            digiproduct_form = DigiProductForm()  # فرم جدید برای خالی شدن
    else:
        digiproduct_form = DigiProductForm()
    return render(request, 'sale/add_digiinvoice_items.html', {
        'invoice': invoice,
        'digiproduct_form': digiproduct_form,
    })
# --------------------------------------------------------

@login_required
def add_digipayment(request, digiinvoice_id):
    invoice = get_object_or_404(DigiInvoice, id=digiinvoice_id)  # دریافت فاکتور
    if request.method == 'POST':
        payment_form = DigiPaymentForm(request.POST)
        jalali_date = payment_form.data['pay_date']
        try:
            formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            payment_form.data = payment_form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
            payment_form.data['pay_date'] = formatted_date
        except ValueError:
            payment_form.add_error('pay_date', 'تاریخ وارد شده نامعتبر است.')
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)  # نجات داده بدون ذخیره
            payment.digiinvoice = invoice  # ارتباط با فاکتور
            payment.save()  # ذخیره پرداخت
            return redirect('sale:add_digipayment', digiinvoice_id=invoice.id)
    else:
        payment_form = DigiPaymentForm()
    return render(request, 'sale/add_digipayment.html', {
        'payment_form': payment_form,
        'invoice': invoice,
    })
# ------------------------------------------------------

@login_required
def digisale_detail(request, digiinvoice_id):
    digiinvoice = get_object_or_404(DigiInvoice, pk=digiinvoice_id)
    items = digiinvoice.digiitems.all()
    payments = digiinvoice.digipayments.all()
    total_digipaid = sum(payment.digiamount for payment in payments)
    total_digidiscount = sum(payment.digidiscount or 0 for payment in payments)
    total_digiprice = sum(item.digiprice or 0 for item in items)
    remaining_digiamount = total_digiprice - total_digipaid - total_digidiscount
    context = {
        'digiinvoice': digiinvoice,
        'items': items,
        'payments': payments,
        'total_digipaid':total_digipaid,
        'total_digidiscount':total_digidiscount,
        'total_digiprice':total_digiprice,
        'remaining_digiamount': remaining_digiamount,
    }
    return render(request, 'sale/digisale_detail.html', context)


# ================================PDF VIEWE==============

# تابع مربوط به نمایش فارسی فونت
def reshape_text(text):
    reshaped_text = arabic_reshaper.reshape(text)  # اصلاح حروف فارسی
    bidi_text = get_display(reshaped_text)  # مرتب‌سازی راست‌به‌چپ
    return bidi_text

def pdf_goldsale_detail(request, invoice_id):
    font_path = 'static/assets/css/fonts/Vazirmatn-Light.ttf'
    pdfmetrics.registerFont(TTFont('Vazirmatn-Medium', font_path))
    invoice = get_object_or_404(GoldInvoice, id=invoice_id)
    items = invoice.golditems.all()
    payments = invoice.payments.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    # عنوان فاکتور
    p.setFont("Vazirmatn-Medium", 16)
    p.drawString(220, height - 50, reshape_text("فاکتور فروش"))
    # اطلاعات مشتری
    p.setFont("Vazirmatn-Medium", 12)
    customer_name = f"نام مشتری: {invoice.customersale.first_name} {invoice.customersale.last_name}"
    customer_mellicod = f"کد ملی: {invoice.customersale.mellicode}"
    date_string = invoice.date.strftime('%Y/%m/%d')  # فرمت تاریخ به دلخواه شما

    p.drawString(220, height - 80, reshape_text(customer_name))
    p.drawString(220, height - 100, reshape_text(customer_mellicod))
    p.drawString(220, height - 120, reshape_text(f" تاریخ خرید: {date_string}"))
    p.drawString(220, height - 140,reshape_text(f"فروشنده: {(invoice.seller)}"))
# ---------------------------------------
    # تنظیمات جدول اول
    table_data_1 = [[reshape_text("کد کالا"), reshape_text("نام کالا"), reshape_text("وزن"),
                     reshape_text("اجرت فروش"), reshape_text("سود فروشنده")]]
    for item in items:
        table_data_1.append(
            [item.goldcode,
             reshape_text(item.goldname),
             item.weight,
             item.sale_ojrat,
             item.seller_benefit])
    row_heights = [20] * len(table_data_1)  # برای مثال، 30 واحد برای هر ردیف
    table_1 = Table(table_data_1, colWidths=[100, 200, 60, 60, 60], rowHeights=row_heights)
    table_1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Vazirmatn-Medium'),  # تنظیم فونت برای تمام سلول‌ها
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table_1.wrapOn(p, width, height)
    table_1.drawOn(p, 50, height - 350)
        # ----------------------------------
    # تنظیمات جدول دوم
    table_data_2 = [[reshape_text("قیمت روز طلا"), reshape_text("مالیات"), reshape_text("قیمت محاسبه طلا"),
                     reshape_text("قیمت ریالی کالا")]]
    for item in items:
        table_data_2.append([f"{item.daily_price:,}",
                             f"{item.sale_tax:,}",
                             f"{item.calcu_amount:,}",
                             f"{item.price:,}"])
    row_heights = [20] * len(table_data_2)  # برای مثال، 30 واحد برای هر ردیف
    table_2 = Table(table_data_2, colWidths=[120, 120, 120, 120], rowHeights=row_heights)
    table_2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Vazirmatn-Medium'),  # تنظیم فونت برای تمام سلول‌ها
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table_2.wrapOn(p, width, height)
    table_2.drawOn(p, 50, height - 550)
    # ترسیم جدول پرداخت‌ها
    table_data_3 = [[reshape_text("تاریخ پرداخت"), reshape_text("روش پرداخت"), reshape_text("تخفیف"),
                     reshape_text("کد تخفیف"), reshape_text("اعتبار"), reshape_text("کد اعتبار"),
                     reshape_text("شرح پرداخت"), reshape_text("مبلغ پرداخت")]]
    for payment in payments:
        payment_explain = str(payment.payment_explain) if payment.payment_explain is not None else ''
        table_data_3.append([payment.pay_date,
                             payment.payment_method,
                             payment.discount,
                             payment.discount_code,
                             f"{payment.etebar if payment.etebar is not None else 0:,}",
                             payment.etebar_code,
                             reshape_text(payment_explain),
                             f"{payment.amount if payment.amount is not None else 0:,}"])
    row_heights = [20] * len(table_data_3)
    table_3 = Table(table_data_3, colWidths=[70, 50, 50, 50, 70, 60, 60, 70], rowHeights=row_heights)
    table_3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Vazirmatn-Medium'),  # تنظیم فونت برای تمام سلول‌ها
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table_3.wrapOn(p, width, height)
    table_3.drawOn(p, 50, height - 750)
    # بستن صفحه و ذخیره
    p.showPage()
    p.save()
    return response


# -----------------------------------------
def reshape_text(text):
    reshaped_text = arabic_reshaper.reshape(text)  # اصلاح حروف فارسی
    bidi_text = get_display(reshaped_text)  # مرتب‌سازی راست‌به‌چپ
    return bidi_text

def pdf_digisale_detail(request, digiinvoice_id):
    if digiinvoice_id is None:  # چک کردن معتبر بودن invoice_id
        raise Http404("فاکتور یافت نشد.")
    font_path = 'static/assets/css/fonts/Vazirmatn-Light.ttf'
    pdfmetrics.registerFont(TTFont('Vazirmatn-Medium', font_path))
    invoice = get_object_or_404(DigiInvoice, id=digiinvoice_id)
    items = invoice.digiitems.all()
    payments = invoice.digipayments.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="فاکتور فروش_{invoice.id}.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    # عنوان فاکتور
    p.setFont("Vazirmatn-Medium", 16)
    p.drawString(220, height - 50, reshape_text("فاکتور فروش"))
    # اطلاعات مشتری
    p.setFont("Vazirmatn-Medium", 12)
    customer_name = f"نام مشتری: {invoice.customersale.first_name} {invoice.customersale.last_name}"
    customer_mellicod = f"کد ملی: {invoice.customersale.mellicode}"
    date_string = invoice.date.strftime('%Y/%m/%d')  # فرمت تاریخ به دلخواه شما

    p.drawString(220, height - 80, reshape_text(customer_name))
    p.drawString(220, height - 100, reshape_text(customer_mellicod))
    p.drawString(220, height - 120, reshape_text(f" تاریخ خرید: {date_string}"))
    p.drawString(220, height - 140,reshape_text(f"فروشنده: {(invoice.seller)}"))
# ---------------------------------------
    total_digiprice = invoice.total_digiprice
    p.setFont("Vazirmatn-Medium", 12)
    total_text = reshape_text(f"مبلغ کل فاکتور: {total_digiprice:,} تومان")
    p.drawString(220, height - 170 , total_text)
    # ----------------------------
    # تنظیمات جدول اول
    table_data_1 = [[reshape_text("کد کالا"), reshape_text("نام کالا"), reshape_text("مدل"),
                     reshape_text("برند"), reshape_text("رنگ")]]
    for item in items:
        table_data_1.append(
            [item.digicode,
             reshape_text(item.diginame),
             reshape_text(item.model),
             reshape_text(item.brand),
             reshape_text(item.color)])
    row_heights = [20] * len(table_data_1)  # برای مثال، 30 واحد برای هر ردیف
    table_1 = Table(table_data_1, colWidths=[100, 140, 140, 50, 50], rowHeights=row_heights)
    table_1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Vazirmatn-Medium'),  # تنظیم فونت برای تمام سلول‌ها
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table_1.wrapOn(p, width, height)
    table_1.drawOn(p, 50, height - 350)
        # ----------------------------------
    # تنظیمات جدول دوم
    table_data_2 = [[reshape_text("تعداد"), reshape_text("مالیات"), reshape_text("قیمت واحد"),
                     reshape_text("قیمت کالا")]]
    for item in items:
        table_data_2.append([f"{item.qty if item.qty is not None else 1:,}",
                             f"{item.sale_tax if item.sale_tax is not None else 0:,}",
                             f"{item.digiprice if item.digiprice is not None else 0:,}",
                             f"{(item.digiprice if item.digiprice is not None else 0) * (item.qty if item.qty is not None else 1):,}"])
    row_heights = [20] * len(table_data_2)  # برای مثال، 30 واحد برای هر ردیف
    table_2 = Table(table_data_2, colWidths=[120, 120, 120, 120], rowHeights=row_heights)
    table_2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Vazirmatn-Medium'),  # تنظیم فونت برای تمام سلول‌ها
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table_2.wrapOn(p, width, height)
    table_2.drawOn(p, 50, height - 550)
    # ترسیم جدول پرداخت‌ها
    table_data_3 = [[reshape_text("تاریخ پرداخت"), reshape_text("روش پرداخت"), reshape_text("تخفیف"),
                     reshape_text("کد تخفیف"), reshape_text("اعتبار"), reshape_text("کد اعتبار"),
                     reshape_text("شرح پرداخت"), reshape_text("مبلغ پرداخت")]]
    for payment in payments:
        payment_explain = str(payment.payment_explain) if payment.payment_explain is not None else ''
        table_data_3.append([payment.pay_date,
                             payment.payment_method,
                             payment.digidiscount,
                             payment.discount_code,
                             f"{payment.etebar if payment.etebar is not None else 0:,}",
                             payment.etebar_code,
                             reshape_text(payment_explain),
                             f"{payment.digiamount if payment.digiamount is not None else 0:,}"])
    row_heights = [20] * len(table_data_3)
    table_3 = Table(table_data_3, colWidths=[70, 50, 50, 50, 70, 60, 60, 70], rowHeights=row_heights)
    table_3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Vazirmatn-Medium'),  # تنظیم فونت برای تمام سلول‌ها
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table_3.wrapOn(p, width, height)
    table_3.drawOn(p, 50, height - 750)
    # بستن صفحه و ذخیره
    p.showPage()
    p.save()
    return response


