from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from .models import BuyInvoice,BuyItem
from accounts.models import Supplier
from .forms import BuyInvoiceForm,BuyItemForm
import jdatetime
from django.db.models import Count
from django.db.models import Q, Exists, OuterRef, Subquery, Max, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import BuyItem, Inventory





# ---------------------------------ایجاد فاکتور خرید ---------------

@login_required
def create_buyinvoice(request):
    if request.method == 'POST':
        form = BuyInvoiceForm(request.POST)

        jalali_date = request.POST.get('date')
        if jalali_date:
            try:
                formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
                form.data = form.data.copy()
                form.data['date'] = formatted_date
            except ValueError:
                messages.error(request, 'تاریخ وارد شده نامعتبر است.')
                return render(request, 'storage/create_buyinvoice.html', {'form': form})

        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.save()
            return redirect('storage:buyinvoice_list')
    else:
        form = BuyInvoiceForm()
    return render(request, 'storage/create_buyinvoice.html', {'form': form})

# ---------------------------------------


@login_required
def buyinvoice_list(request):
    if request.GET:
        request.session['buyinvoice_list_filters'] = {
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
            'supply_name': request.GET.get('supply_name', ''),

        }

    filters = request.session.get('buyraw_invoice_list_filters', {})
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')
    supply_name = filters.get('supply_name', '')

    invoices = BuyInvoice.objects.all()
    start_date_jalali = ''
    end_date_jalali = ''

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

    if supply_name:
        invoices = invoices.filter(
            Q(supplier__first_name__icontains=supply_name) |
            Q(supplier__last_name__icontains=supply_name)
        )

        suppliers = Supplier.objects.filter(
            Q(first_name__icontains=supply_name) |
            Q(last_name__icontains=supply_name)
        )

    invoices = invoices.order_by('-date')
    if not (start_date or end_date or supply_name):
        invoices = invoices[:10]

    context = {
        'invoices': invoices,
        'supply_name': supply_name,
        'filters': filters,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
    }
    return render(request, 'storage/buyinvoice_list.html', context)
# ---------------------------------------------


@login_required
def register_buyitem(request, invoice_id):
    invoice = get_object_or_404(BuyInvoice, id=invoice_id)
    items = BuyItem.objects.filter(invoice=invoice)

    if request.method == 'POST':
        form = BuyItemForm(request.POST)
        if form.is_valid():
            buy_item = form.save(commit=False)
            buy_item.invoice = invoice
            buy_item.save()
            messages.success(request, "کالای خرید با موفقیت ثبت شد.")
            return redirect(reverse('storage:register_buyitem', args=[invoice_id]))
        else:
            messages.error(request, "لطفاً فرم را به درستی پر کنید.")
    else:
        form = BuyItemForm()

    return render(request, 'storage/register_buyitem.html', {
        'form': form,
        'invoice': invoice,
        'items': items,
    })

# -------------------------------------------


@login_required
def storage_list(request):
    if request.GET:
        request.session['storage_filters'] = {
            'name': request.GET.get('name', ''),
            'code': request.GET.get('code', ''),
        }

    filters = request.session.get('storage_filters', {})
    name = filters.get('name', '')
    code = filters.get('code', '')

    # فیلتر اولیه
    item_filter = Q()
    if name:
        item_filter &= Q(item__name__icontains=name)
    if code:
        item_filter &= Q(item__sku__icontains=code)

    # گرفتن آیتم‌هایی که در انبار وجود دارند
    inventory_items = Inventory.objects.values_list('item', flat=True)

    # گروه‌بندی buyitemها بر اساس item و گرفتن یک نمونه از هر گروه
    filtered_items = (
        BuyItem.objects.filter(item__in=inventory_items)
        .filter(item_filter)
        .values('item')
        .annotate(
            sample_id=Max('id'),  # آخرین نمونه
            total_count=Count('id')  # تعداد کل
        )
    )

    # گرفتن خود buyitemها بر اساس sample_id
    sample_ids = [obj['sample_id'] for obj in filtered_items]
    sample_buyitems = BuyItem.objects.filter(id__in=sample_ids).select_related('item')

    # ساخت دیکشنری item_id -> total_count
    count_dict = {obj['item']: obj['total_count'] for obj in filtered_items}

    # صفحه‌بندی
    paginator = Paginator(sample_buyitems, 20)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    # سبد فروش
    cart = request.session.get('sale_cart', [])
    cart_count = len(cart)

    context = {
        'page_obj': page_obj,
        'name': name,
        'code': code,
        'filters': filters,
        'cart_count': cart_count,
        'items': page_obj,
        'count_dict': count_dict,  # تعداد کل برای هر آیتم
    }
    return render(request, 'storage/storage_list.html', context)

# -----------------------------------------
from .forms import UploadImageForm

@login_required
def cart_detail(request,item_id):
    item = None
    form = UploadImageForm()
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            item.image = form.cleaned_data['image']
            item.save()
            messages.success(request, "تصویر با موفقیت آپلود شد.")
            return redirect('storage:cart_detail',  item_id=item_id)
        else:
            messages.error(request, "خطا در آپلود تصویر. لطفاً مجدداً تلاش کنید.")

    return render(request, 'storage/cart_detail.html', {'item': item, 'form': form})

# -------------------------------