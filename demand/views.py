
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from jdatetime import datetime as jdatetime
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth

from .models import Loan, Installment, Repayment, Guarantee
from .forms import LoanForm, GuaranteeForm, InstallmentForm, RepaymentForm,UpdateInstallmentForm
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Loan
from django.db.models import Q
from django.db.models import Sum, F, Prefetch
import jdatetime


# ---------------------------------------------
@login_required
def demand(request):
    today = timezone.now().date()
    if request.GET:
        request.session['demand_filters'] = {
            'customer': request.GET.get('customer', ''),
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
        }
    filters = request.session.get('demand_filters', {})
    customer_name = filters.get('customer', '')
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')
    installments = Installment.objects.filter(paid=False, due_date__gte=today).select_related(
        'loan__customer').order_by('due_date')
    start_date_jalali = ''
    end_date_jalali = ''
    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()
        installments = installments.filter(
            paid=False,
            due_date__gt=today,
            due_date__range=(start_date_gregorian, end_date_gregorian)
        ).select_related('loan__customer').order_by('due_date')
        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y-%m-%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y-%m-%d')

    if customer_name:
        installments = installments.filter(
            Q(loan__customer__last_name__icontains=customer_name) |
            Q(loan__customer__first_name__icontains=customer_name)
        )
    total_amount = installments.aggregate(Sum('amount'))['amount__sum'] or 0
    context = {
        'installments': installments,
        'total_amount': total_amount,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'customer_name': customer_name,
        'filters': filters,
    }
    return render(request, 'demand/demand.html', context)


# ========================================================
@login_required
def demand_vosoli(request):
    today = timezone.now().date()
    customer_name = request.GET.get('customer')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    installments = Installment.objects.filter(paid=True ).select_related(
        'loan__customer').order_by('-due_date')
    start_date_jalali = ''
    end_date_jalali = ''
    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()

        installments = installments.filter(
            paid=True,
            due_date__range=(start_date_gregorian, end_date_gregorian)
        ).select_related('loan__customer').order_by('-due_date')
        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y-%m-%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y-%m-%d')
    if customer_name:
        installments = installments.filter(
            Q(loan__customer__last_name__icontains=customer_name) |
            Q(loan__customer__first_name__icontains=customer_name)
        )
    total_amount = installments.aggregate(Sum('amount'))['amount__sum'] or 0
    context = {
        'installments': installments,
        'total_amount': total_amount,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'customer_name': customer_name,
    }
    return render(request, 'demand/demand_vosoli.html', context)

# ----------------------------------------------------------
@login_required
def demand_remain(request):
    today = timezone.now().date()
    if request.GET:
        request.session['demand_remain_filters'] = {
            'customer': request.GET.get('customer', ''),
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
        }

    filters = request.session.get('demand_remain_filters', {})
    customer = filters.get('customer', '')
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')

    moavagh_installments = Installment.objects.filter(
        paid=False, due_date__lt=today
    ).select_related('loan__customer').order_by('due_date')

    start_date_jalali = ''
    end_date_jalali = ''
    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))
        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()
        moavagh_installments = moavagh_installments.filter(
            due_date__range=(start_date_gregorian, end_date_gregorian)
        )
        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y-%m-%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y-%m-%d')
    if customer:
        moavagh_installments = moavagh_installments.filter(
            Q(loan__customer__last_name__icontains=customer) |
            Q(loan__customer__first_name__icontains=customer)
        )
    total_movagh = moavagh_installments.aggregate(Sum('amount'))['amount__sum'] or 0
    context = {
        'moavagh_installments': moavagh_installments,
        'total_movagh': total_movagh,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'customer_name': customer,
        'filters': filters,
    }
    return render(request, 'demand/demand_remain.html', context)


# =========================================================
@login_required
def create_loan(request):
    if request.method == 'POST':
        loan_form = LoanForm(request.POST)
        dates_to_convert = ['loan_date', 'start_date', 'end_date']
        for date_field in dates_to_convert:
            jalali_date = loan_form.data.get(date_field)
            if jalali_date:
                try:
                    formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
                    loan_form.data = loan_form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
                    loan_form.data[date_field] = formatted_date
                except ValueError:
                    loan_form.add_error(date_field, f'تاریخ {date_field} نامعتبر است.')
        if loan_form.is_valid():
            loan = loan_form.save(commit=False)
            loan.save()
            messages.success(request, 'وام با موفقیت ثبت شد')
            return redirect('demand:loan_list')
        else:
            print("Form is not valid: ", loan_form.errors)
    else:
        loan_form = LoanForm()
    context = {
        'loan_form': loan_form,
    }
    return render(request, 'demand/create_loan.html', context)


# ================================================


@login_required
def create_zemanat(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    if request.method == 'POST':
        zemanat_form = GuaranteeForm(request.POST)
        jalali_date = zemanat_form.data['guarantee_date']
        try:

            formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            zemanat_form.data = zemanat_form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
            zemanat_form.data['guarantee_date'] = formatted_date
        except ValueError:
            zemanat_form.add_error('guarantee_date', 'تاریخ وارد شده نامعتبر است.')
        if zemanat_form.is_valid():
            zemanat = zemanat_form.save(commit=False)
            zemanat.loan = loan  # ارتباط دادن ضمانت با وام مربوطه
            zemanat.save()
            messages.success(request, 'ضمانت با موفقیت ثبت شد')
            zemanat_form = GuaranteeForm()
    else:
        zemanat_form = GuaranteeForm()
    context = {
        'zemanat_form': zemanat_form,
        'loan': loan,
    }
    return render(request, 'demand/create_zemanat.html', context)


# ===========================================
#
@login_required
def loan_list(request):
    if request.GET:
        request.session['loan_list_filters'] = {
            'start_date': request.GET.get('start_date', ''),
            'end_date': request.GET.get('end_date', ''),
            'customer': request.GET.get('customer', ''),
            'plan': request.GET.get('plan', ''),
        }
    filters = request.session.get('loan_list_filters', {})
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')
    customer_name = filters.get('customer', '')
    loan_plan = filters.get('plan', '')
    loans = Loan.objects.filter(tasviye_status=False)
    start_date_jalali = ''
    end_date_jalali = ''

    if start_date and end_date:
        start_date = start_date.replace('/', '-')
        end_date = end_date.replace('/', '-')
        start_year, start_month, start_day = map(int, start_date.split('-'))
        end_year, end_month, end_day = map(int, end_date.split('-'))

        start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
        end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()

        loans = loans.filter(loan_date__range=(start_date_gregorian, end_date_gregorian))

        start_date_jalali = jdatetime.date.fromgregorian(date=start_date_gregorian).strftime('%Y/%m/%d')
        end_date_jalali = jdatetime.date.fromgregorian(date=end_date_gregorian).strftime('%Y/%m/%d')


    if customer_name:
        loans = loans.filter(
            Q(customer__last_name__icontains=customer_name) |
            Q(customer__first_name__icontains=customer_name)
        )

    if loan_plan:
        loans = loans.filter(plan=loan_plan)

    loans = loans.prefetch_related(
        Prefetch('installments'),
        Prefetch('guarantees')
    ).order_by('-loan_date')

    if not (start_date or end_date or customer_name or loan_plan):
        loans = loans[:10]

    for loan in loans:
        total_amount = loan.total_amount or 0
        final_amount = loan.final_amount or 0
        num_month = loan.num_month or 1  # جلوگیری از تقسیم بر صفر

        # سود کل
        profit = final_amount - total_amount

        # سود ماهانه ریالی
        monthly_profit = profit / num_month if num_month else 0

        # درصد سود ماهانه
        monthly_interest_percent = ((profit / total_amount) / num_month * 100) if total_amount else 0

        # افزودن به شیء وام
        loan.profit = profit
        loan.monthly_profit = monthly_profit
        loan.monthly_interest_percent = monthly_interest_percent

    total_amount_sum = loans.aggregate(total_amount_sum=Sum('total_amount'))['total_amount_sum'] or 0
    final_amount_sum = loans.aggregate(final_amount_sum=Sum('final_amount'))['final_amount_sum'] or 0
    profit_sum = final_amount_sum - total_amount_sum

    # درصد سود کلی (نسبت به کل اصل وام‌ها)
    total_profit_percent = (profit_sum / total_amount_sum * 100) if total_amount_sum else 0
    context = {
        'loans': loans,
        'total_amount_sum': total_amount_sum,
        'final_amount_sum': final_amount_sum,
        'profit_sum': profit_sum,
        'total_profit_percent': total_profit_percent,
        'start_date': start_date_jalali,
        'end_date': end_date_jalali,
        'customer_name': customer_name,
        'loan_plan': loan_plan,
        'filters': filters,
    }
    return render(request, 'demand/loan_list.html', context)




# ----------------------------------------------


def export_loans_excel(request):
    filters = request.session.get('loan_list_filters', {})
    start_date = filters.get('start_date', '')
    end_date = filters.get('end_date', '')
    customer_name = filters.get('customer', '')

    loans = Loan.objects.filter(tasviye_status=False)

    # فیلتر بر اساس تاریخ شمسی
    if start_date and end_date:
        try:
            start_date = start_date.replace('/', '-')
            end_date = end_date.replace('/', '-')
            start_year, start_month, start_day = map(int, start_date.split('-'))
            end_year, end_month, end_day = map(int, end_date.split('-'))

            start_date_gregorian = jdatetime.date(start_year, start_month, start_day).togregorian()
            end_date_gregorian = jdatetime.date(end_year, end_month, end_day).togregorian()

            loans = loans.filter(loan_date__range=(start_date_gregorian, end_date_gregorian))
        except Exception:
            pass  # اگر تبدیل تاریخ به هر دلیلی خطا داد، از فیلتر تاریخ صرف‌نظر کن

    # فیلتر بر اساس نام مشتری
    if customer_name:
        loans = loans.filter(
            Q(customer__first_name__icontains=customer_name) |
            Q(customer__last_name__icontains=customer_name)
        )

    loans = loans.select_related("customer")

    # ایجاد فایل اکسل
    wb = Workbook()
    ws = wb.active
    ws.title = "لیست وام‌ها"

    # نوشتن سرفصل‌ها
    ws.append([
        "کد وام",
        "نام مشتری",
        "کد ملی",
        "تاریخ وام",
        "مبلغ کل وام (تومان)",
        "مبلغ نهایی پرداختی (تومان)",
        "تعداد اقساط",
        "وضعیت طرح"
    ])

    # نوشتن ردیف‌ها
    for loan in loans:
        ws.append([
            loan.loan_code or "نامشخص",
            f"{loan.customer.first_name} {loan.customer.last_name}",
            loan.customer.mellicode,
            loan.loan_date.strftime('%Y/%m/%d') if loan.loan_date else "نامشخص",
            loan.total_amount,
            loan.final_amount,
            loan.num_installments,
            loan.plan or "نامشخص"
        ])

    # بازگشت فایل به صورت پاسخ دانلود
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=loan_list.xlsx'
    wb.save(response)
    return response

# =========================================
# تابع نمایش جزییات وام
@login_required
def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    installments = Installment.objects.filter(loan=loan).order_by('due_date')
    guarantees = Guarantee.objects.filter(loan=loan)
    mande_moavagh = loan.calculate_mande_moavagh()
    repayments = Repayment.objects.filter(installment__loan=loan).order_by('repayment_date')
    context = {
        'loan': loan,
        'installments': installments,
        'mande_moavagh': mande_moavagh,
        'repayments': repayments,
        'guarantees': guarantees,
    }
    return render(request, 'demand/loan_detail.html', context)



# -------------------------------------------------------

# تابع افزودن ماه به جدول اقساط
def add_months(start_date, months):
    z_mah = start_date.month
    z_year = start_date.year
    z_day = start_date.day

    if z_mah > 12:
        z_mah = z_mah - 12
        z_year = z_year + 1
    fu_mah = months + z_mah
    if fu_mah > 12:
        t_mah = fu_mah - 12
        t_year = z_year + 1
    else:
        t_mah = fu_mah
        t_year = z_year
        # بررسی 30 روزه بودن 6 ماهه دوم سال
    if t_mah >= 7 and t_mah <= 11 and z_day == 31:
        z_day = 30
    if t_mah == 12 and (z_day == 31 or z_day == 30):
        z_day = 29
    final_date = start_date.replace(month=t_mah, year=t_year, day=z_day)
    return final_date


# =========================================

# ایجاد جدول اقساط
from django.db import transaction

@login_required
def create_installments(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    # چک کردن اینکه اقساط قبلاً ایجاد شده‌اند یا خیر
    if loan.installments_created:
        messages.error(request, "جدول اقساط قبلا ایجاد شده است")
        return redirect(reverse('demand:loan_detail', args=[loan_id]))
    if loan.final_amount is None or loan.num_installments is None or loan.num_installments == 0:
        messages.error(request, "اطلاعات وام کامل نیست.")
        return redirect(reverse('demand:loan_detail', args=[loan_id]))
    installment_amount = int(loan.final_amount / loan.num_installments)
    start_date = loan.start_date
    first_ghest_count = 1
    try:
        with transaction.atomic():
            # دوباره چک می‌کنیم که اقساط ایجاد نشده باشند
            loan.refresh_from_db()
            if loan.installments_created:
                messages.error(request, "جدول اقساط قبلا ایجاد شده است")
                return redirect(reverse('demand:loan_detail', args=[loan_id]))
            # ایجاد اقساط به تعداد num_installments
            for i in range(0, loan.num_installments):
                due_date = add_months(start_date, i)
                Installment.objects.create(
                    loan=loan,
                    amount=installment_amount,
                    due_date=due_date,
                    ghest_count=first_ghest_count + i
                )
            loan.installments_created = True
            loan.save()
        messages.success(request, "جدول اقساط با موفقیت ایجاد شد.")
    except Exception as e:
        messages.error(request, "خطا در ایجاد اقساط. لطفاً دوباره تلاش کنید.")
    return redirect(reverse('demand:loan_detail', args=[loan_id]))
# --------------------------------------------



def update_installments(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    installment_forms = []
    installments = loan.installments.all().order_by('ghest_count')  # اضافه کردن مرتب‌سازی
    if request.method == 'POST':
        is_valid = True
        for installment in installments:  # استفاده از اقساط مرتب‌شده
            form = UpdateInstallmentForm(request.POST, instance=installment, prefix=f'installment_{installment.id}')
            if form.is_valid():
                form.save()
            else:
                is_valid = False
            installment_forms.append({
                'form': form,
                'id': installment.id,
                'ghest_count': installment.ghest_count,
            })
        if is_valid:
            return redirect('demand:loan_detail', loan_id=loan.id)
    else:
        for installment in installments:  # استفاده از اقساط مرتب‌شده
            form = UpdateInstallmentForm(instance=installment, prefix=f'installment_{installment.id}')
            installment_forms.append({
                'form': form,
                'id': installment.id,
                'ghest_count': installment.ghest_count,
            })

    return render(request, 'demand/update_installments.html', {
        'loan': loan,
        'installment_forms': installment_forms,
    })



# =============================================

@login_required
def create_repayment(request, installment_id=None):
    installment = get_object_or_404(Installment, pk=installment_id)
    loan_id = installment.loan.id
    mande_moavagh_ghest = installment.calculate_mande_moavagh_ghest()
    if request.method == 'POST':
        form = RepaymentForm(request.POST)
        jalali_date = form.data['repayment_date']
        try:
            formatted_date = jdatetime.datetime.strptime(jalali_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            form.data = form.data.copy()  # داده‌های فرم باید قابل ویرایش باشند
            form.data['repayment_date'] = formatted_date
        except ValueError:
            form.add_error('repayment_date', 'تاریخ وارد شده نامعتبر است.')
        if form.is_valid():
            repayment = form.save(commit=False)
            repayment.installment = installment
            repayment.save()
            return redirect('demand:demand')
    else:
        form = RepaymentForm(initial={'installment': installment})

    context = {
        'form': form,
        'installment': installment,
        'loan_id': loan_id,
        'mande_moavagh_ghest': mande_moavagh_ghest,
    }
    return render(request, 'demand/create_repayment.html', context)


# ============================================

def reshape_text(text):
    # این تابع برای سازگاری با فارسی است
    reshaped_text = reshape(text)
    return get_display(reshaped_text)


def pdf_loan_agreement(request, loan_id):
    font_path = 'static/assets/css/fonts/Vazirmatn-Light.ttf'
    pdfmetrics.registerFont(TTFont('Vazirmatn-Medium', font_path))
    loan = get_object_or_404(Loan, id=loan_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="loan_agreement{loan.id}.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    styles = getSampleStyleSheet()
    normal_style = ParagraphStyle(
        name="Normal",
        fontName="Vazirmatn-Medium",
        fontSize=12,
        leading=14,  # فاصله بین خطوط
        rightIndent=40,  # تنظیم برای راست‌چین کردن متن
        alignment=2,  # تنظیم برای راست‌چین کردن
    )

    p.setFont("Vazirmatn-Medium", 10)
    p.drawString(250, height - 50, reshape_text("بسمه تعالی"))

    p.setFont("Vazirmatn-Medium", 14)  # استفاده از فونت بولد
    p.drawString(200, height - 80, reshape_text("قرارداد اعطای وام خرید کالا و خدمات"))

    p.setFont("Vazirmatn-Medium", 11)
    p.drawString(50, height - 140, reshape_text(f"تاریخ قرارداد: {loan.loan_date.strftime('%Y/%m/%d')}"))

    text = reshape_text(f"طرف اول:")
    text_width = stringWidth(text, "Vazirmatn-Medium", 14)
    p.drawString(width - 30 - text_width, height - 150, text)

    text = reshape_text(
        f" خانم/آقای  {loan.customer.first_name} {loan.customer.last_name} با کد ملی {loan.customer.mellicode}  ")
    text_width = stringWidth(text, "Vazirmatn-Medium", 11)
    p.drawString(width - 40 - text_width, height - 180, text)

    text = reshape_text(f" طرف دوم:")
    text_width = stringWidth(text, "Vazirmatn-Medium", 14)
    p.drawString(width - 30 - text_width, height - 210, text)

    text = reshape_text(
        f" شرکت تجارت افرین پانیا(سهامی خاص) با نام تجاری تاپ قسطی به شماره ثبت 392.")
    text_width = stringWidth(text, "Vazirmatn-Medium", 11)
    p.drawString(width - 40 - text_width, height - 240, text)

    text = reshape_text(f" مبلغ قرارداد :")
    text_width = stringWidth(text, "Vazirmatn-Medium", 14)
    p.drawString(width - 30 - text_width, height - 270, text)

    formatted_total_amount = f"{loan.total_amount:,}"
    text = reshape_text(
        f" مبلغ {formatted_total_amount} تومان بعنوان اعتبار خرید اقساطی کالا و خدمات که به طرف اول پرداخت گردیده است. ")
    text_width = stringWidth(text, "Vazirmatn-Medium", 11)
    p.drawString(width - 40 - text_width, height - 300, text)

    text = reshape_text(f" نحوه بازپرداخت :")
    text_width = stringWidth(text, "Vazirmatn-Medium", 14)
    p.drawString(width - 30 - text_width, height - 330, text)

    formatted_final_amount = f"{loan.final_amount:,}"
    text = reshape_text(
        f" مبلغ {formatted_final_amount} تومان که میبایست طرف اول در تعداد اقساط {loan.num_installments}ماهه به حساب طرف دوم واریز نماید. ")
    text_width = stringWidth(text, "Vazirmatn-Medium", 11)
    p.drawString(width - 40 - text_width, height - 360, text)

    text = reshape_text(f" تعهدات طرفین : ")
    text_width = stringWidth(text, "Vazirmatn-Medium", 14)
    p.drawString(width - 30 - text_width, height - 390, text)

    text = reshape_text(f"1-طرف اول متعهد می‌شود که اقساط خود را در سررسیدهای تعیین شده به طرف دوم پرداخت نماید .")
    text_width = stringWidth(text, "Vazirmatn-Medium", 11)
    p.drawString(width - 40 - text_width, height - 420, text)

    text = reshape_text(
        f"2-طرف دوم میتواند درصورت عدم پرداخت بدهی طرف اول در موقع مقرر، جریمه تأخیر تأدیه رااز وی مطالبه نماید.")
    text_width = stringWidth(text, "Vazirmatn-Medium", 11)
    p.drawString(width - 40 - text_width, height - 450, text)

    text = reshape_text(
        f"3-درصورت عدم پرداخت اقساط در موعد مقرر طرف دوم میتواند نسبت به وصول آن از محل تضامین طرف اول اقدام نماید.")
    text_width = stringWidth(text, "Vazirmatn-Medium", 11)
    p.drawString(width - 40 - text_width, height - 480, text)

    text = reshape_text(
        f"4-طرف دوم میتواند کلیه هزینه های اداری و حقوقی مانند هزینه وکالت و دادرسی را از محل تضامین طرف اول مطالبه نماید.")
    text_width = stringWidth(text, "Vazirmatn-Medium", 11)
    p.drawString(width - 40 - text_width, height - 510, text)

    text = reshape_text(
        f"5-تاییداین قرارداد در هریک از شبکه های اجتماعی یا پلتفرم آنلاین مربوط به طرف دوم به منزله امضا فیزیکی قرارداد میباشد.")
    text_width = stringWidth(text, "Vazirmatn-Medium", 11)
    p.drawString(width - 40 - text_width, height - 540, text)

    text = reshape_text(
        f"6-طرف دوم تعهد مینماید در صورت وصول همه اقساط طرف اول در موعد مقرر تضامین زیر را به وی عودت نماید.")
    text_width = stringWidth(text, "Vazirmatn-Medium", 11)
    p.drawString(width - 40 - text_width, height - 570, text)

    y_position = height - 600
    for guarantee in loan.guarantees.all():
        formatted_guarantee_amount = f"{guarantee.guarantee_amount:,}"
        text = reshape_text(
            f" {guarantee.get_guarantee_type_display()} به شماره سریال {guarantee.guarantee_serial} و به مبلغ {formatted_guarantee_amount} تومان")
        text_width = stringWidth(text, "Vazirmatn-Medium", 12)
        p.drawString(width - 70 - text_width, y_position, text)
        y_position -= 30  # فاصله بین خطوط

    text = reshape_text(f" امضاء طرف اول :")
    text_width = stringWidth(text, "Vazirmatn-Medium", 14)
    p.drawString(width - 100 - text_width, height - 720, text)

    text = reshape_text(f" امضاء نماینده طرف دوم :")
    text_width = stringWidth(text, "Vazirmatn-Medium", 14)
    p.drawString(width - 300 - text_width, height - 720, text)

    p.showPage()
    p.save()
    return response
# -----------------------------------------------------------------------------------
def reshape_text(text):
    # این تابع برای سازگاری با فارسی است
    reshaped_text = reshape(text)
    return get_display(reshaped_text)



def pdf_loan_document(request, loan_id):
    font_path = 'static/assets/css/fonts/Vazirmatn-Light.ttf'
    pdfmetrics.registerFont(TTFont('Vazirmatn-Medium', font_path))
    loan = get_object_or_404(Loan, id=loan_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="loan_document{loan.id}.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    customer = loan.customer
    loan_code = loan.loan_code or "نامشخص"
    plan = loan.plan or "نامشخص"
    loan_date = loan.loan_date.strftime('%Y/%m/%d') if loan.loan_date else "نامشخص"
    start_date = loan.start_date.strftime('%Y/%m/%d') if loan.start_date else "نامشخص"
    end_date = loan.end_date.strftime('%Y/%m/%d') if loan.end_date else "نامشخص"
    total_amount = loan.total_amount or 0
    final_amount = loan.final_amount or 0
    num_month = loan.num_month or 0
    num_installments = loan.num_installments or 0
    first_name = customer.first_name or "نامشخص"
    last_name = customer.last_name or "نامشخص"
    mellicode = customer.mellicode or "نامشخص"
    beta_karmozd = int(final_amount * 0.04) if plan == "بتا" else None
    guarantees = loan.guarantees.all()
    guarantees_data = []
    for guarantee in guarantees:
        guarantees_data.append({
            "guarantor_name": guarantee.guarantor_name or "نامشخص",
            "guarantor_mellicod": guarantee.guarantor_mellicod or "نامشخص",
            "guarantee_type": guarantee.get_guarantee_type_display() or "نامشخص",
            "guarantee_serial": guarantee.guarantee_serial or "نامشخص",
            "guarantee_amount": guarantee.guarantee_amount or 0,
            "guarantee_date": guarantee.guarantee_date.strftime('%Y/%m/%d') if guarantee.guarantee_date else "نامشخص",
            "guarantor_address": guarantee.guarantor_address or "نامشخص",
            "guarantor_phone": guarantee.guarantor_phone or "نامشخص",
        })

    installments = loan.installments.all().order_by('ghest_count')  # مرتب‌سازی اقساط
    installments_data = []
    for installment in installments:
        installments_data.append({
            "ghest_count": installment.ghest_count or 0,
            "amount": installment.amount or 0,
            "due_date": installment.due_date.strftime('%Y/%m/%d') if installment.due_date else "نامشخص",
            "ghest_type": installment.ghest_type or "نامشخص"
        })

    p.setFont("Vazirmatn-Medium", 10)
    p.drawRightString(500, height - 80, reshape_text(
        f"پرونده وام : {first_name} {last_name}      کد ملی: {mellicode}      شناسه وام: {loan_code}"))
    p.drawRightString(500, height - 100, reshape_text(f"طرح وام: {plan}"))
    if beta_karmozd is not None:  # نمایش کارمزد بتا
        p.drawRightString(500, height - 125, reshape_text(f"کارمزد طرح بتا: {beta_karmozd:,} تومان"))
    p.drawRightString(500, height - 150, reshape_text(f"تاریخ وام: {loan_date}"))
    p.drawRightString(500, height - 175, reshape_text(f"اصل وام: {total_amount:,} تومان"))
    p.drawRightString(500, height - 200, reshape_text(f"بازپرداخت نهایی: {final_amount:,} تومان"))
    p.drawRightString(500, height - 225, reshape_text(
        f"تاریخ اولین قسط: {start_date}      تاریخ آخرین قسط: {end_date}"))
    p.drawRightString(500, height - 250, reshape_text(
        f"تعداد قسط: {num_month}      تعداد بازپرداخت: {num_installments}"))
    # جدول افساط
    y_position = height - 300
    p.setFont("Vazirmatn-Medium", 10)
    p.drawRightString(500, y_position, reshape_text("جدول اقساط:"))
    p.line(40, y_position - 5, 560, y_position - 5)
    y_position -= 25
    for installment in installments_data:
        formatted_amount = f"{installment['amount']:,}" if installment['amount'] else 0
        p.drawRightString(500, y_position, reshape_text(
            f" قسط {installment['ghest_count']:02d}      مبلغ: {formatted_amount} تومان      تاریخ سررسید: {installment['due_date']}      نوع قسط: {installment['ghest_type']}"))
        y_position -= 18
    # جذول تضامین
    y_position -= 25  # فاصله بیشتر برای نمایش ضمانت‌ها
    p.setFont("Vazirmatn-Medium", 10)
    p.drawRightString(500, y_position, reshape_text("جدول ضمانت‌ها:"))
    p.line(40, y_position - 5, 560, y_position - 5)
    y_position -= 25
    if guarantees_data:  # اگر ضمانتی وجود داشته باشد
        for guarantee in guarantees_data:
            formatted_amount = f"{guarantee['guarantee_amount']:,}" if guarantee['guarantee_amount'] else 0
            # خط اول: نام ضامن و کد ملی
            p.drawRightString(500, y_position, reshape_text(
                f"ضامن: {guarantee['guarantor_name']}      کد ملی ضامن: {guarantee['guarantor_mellicod']}"))
            y_position -= 18
            # خط دوم: نوع ضمانت و مبلغ ضمانت
            p.drawRightString(500, y_position, reshape_text(
                f"نوع ضمانت: {guarantee['guarantee_type']}      مبلغ ضمانت: {formatted_amount} تومان"))
            y_position -= 18
            # خط سوم: سریال ضمانت و تاریخ ضمانت
            p.drawRightString(500, y_position, reshape_text(
                f"سریال ضمانت: {guarantee['guarantee_serial']}      تاریخ ضمانت: {guarantee['guarantee_date']}"))
            y_position -= 18
            # خط چهارم: آدرس و تلفن ضامن
            p.drawRightString(500, y_position, reshape_text(
                f"آدرس ضامن: {guarantee['guarantor_address']}      تلفن ضامن: {guarantee['guarantor_phone']}"))
            y_position -= 25
            # رسم خط‌چین
            p.setDash(3, 3)  # تنظیم خط‌چین: 3 پیکسل خط، 3 پیکسل فاصله
            p.line(40, y_position, 560, y_position)  # رسم خط‌چین از چپ به راست
            p.setDash([])  # بازنشانی به حالت عادی
            y_position -= 10  # فاصله بین خط‌چین و آیتم بعدی

    else:
        p.drawRightString(500, y_position, reshape_text("هیچ ضمانتی ثبت نشده است."))
        y_position -= 25
    p.showPage()
    p.save()
    return response










