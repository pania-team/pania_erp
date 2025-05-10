
from django.shortcuts import render
from sale.models import GoldProduct,GoldInvoice
from decimal import Decimal
import jdatetime
from django.db.models import Sum, F,Avg








# -------------------------------------------------------------
from decimal import Decimal


def goldreport_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    seller = request.GET.get('seller')
    goldcode = request.GET.get('goldcode')
    invoices = GoldInvoice.objects.prefetch_related('golditems')
    start_date_jalali = ''
    end_date_jalali = ''
    has_filter = bool(start_date or end_date or seller or goldcode)
    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()
        invoices = invoices.filter(date__range=(start_date_gregorian, end_date_gregorian))
        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y/%m/%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y/%m/%d')
    if seller:
        invoices = invoices.filter(seller__name__icontains=seller)
    if goldcode:
        invoices = invoices.filter(golditems__goldcode__icontains=goldcode)
    if has_filter:
        invoices = invoices.order_by('date')
    else:
        invoices = invoices.order_by('-date')[:10]
    invoice_data = []
    all_weight = 0
    total_weighted_benefit = 0
    total_weighted_daily_price = 0
    product_data = []
    for invoice in invoices:
        total_weight = invoice.golditems.aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        invoice.total_weight = total_weight
        for item in invoice.golditems.all():
            if item.sele_benefit is not None and item.weight is not None:
                weighted_benefit = item.sele_benefit * item.weight * Decimal(0.01)
            else:
                weighted_benefit = Decimal(0)
            if item.daily_price is not None and item.weight is not None:
                weighted_daily_price = item.daily_price * item.weight
            else:
                weighted_daily_price = Decimal(0)
            product_data.append({
                'product': item,
                'weighted_benefit': weighted_benefit
            })
            total_weighted_benefit += weighted_benefit
            total_weighted_daily_price += weighted_daily_price
        all_weight += total_weight
        invoice_data.append({
            'invoice': invoice,
        })
    if all_weight > 0:
        weighted_average_daily_price = total_weighted_daily_price / all_weight
    else:
        weighted_average_daily_price = 0
    if all_weight != 0:
        total_profit_percentage = (total_weighted_benefit / all_weight * 100)
    else:
        total_profit_percentage = 0
    invoice_count = len(product_data)
    context = {
        'invoice_data': invoice_data,
        'product_data': product_data,
        'invoice_count': invoice_count,
        'all_weight': all_weight,
        'total_weighted_benefit': total_weighted_benefit,
        'total_profit_percentage': total_profit_percentage,
        'average_daily_price': int(weighted_average_daily_price),
        'start_date_jalali': start_date_jalali,
        'end_date_jalali': end_date_jalali,
    }
    return render(request, 'reports/goldreport_list.html', context)








