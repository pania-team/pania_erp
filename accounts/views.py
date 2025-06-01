from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from .forms import CustomerForm
from .models import HomeImage
from .models import Customer
from django.db.models import Q
from django.urls import reverse



@login_required
def home_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'demand_view': reverse('accounts:demand_view'),
        'storage_view': reverse('accounts:storage_view'),
        'images': {
            'demand_view': 'media/home_images/finance.png',
            'storage_view': 'media/home_images/storage.png',

        },
    }
    return render(request, 'accounts/home.html', context)

# -------------------------------------------
@login_required
def demand_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'create_loan': reverse('demand:create_loan'),
        'loan_list': reverse('demand:loan_list'),
        'demand': reverse('demand:demand'),
        'demand_remain': reverse('demand:demand_remain'),
        'demand_vosoli': reverse('demand:demand_vosoli'),


    }
    return render(request, 'accounts/demand_view.html', context)

# ----------------------------------
@login_required
def storage_view(request):
    try:
        home_image = HomeImage.objects.get(description='home')
    except HomeImage.DoesNotExist:
        home_image = None
    context = {
        'home_image': home_image,
        'create_buyinvoice': reverse('storage:create_buyinvoice'),
        'buyinvoice_list': reverse('storage:buyinvoice_list'),
        'storage_list': reverse('storage:storage_list'),



    }
    return render(request, 'accounts/storage_view.html', context)


# ---------------------------------------------
def user_logout(request):
    logout(request)
    return redirect('accounts:login')  # بعد از لاگ‌اوت به صفحه لاگین هدایت می‌شود


def login_view(request):
    try:
        login_image = HomeImage.objects.get(description='login')
    except HomeImage.DoesNotExist:
        login_image = None
    if request.method == 'POST':
        user_id = request.POST['user_id']
        pass_code = request.POST['pass_code']
        user = authenticate(request, username=user_id, password=pass_code)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')  # هدایت به صفحه demand بعد از ورود موفق
        else:
            messages.error(request, 'رمز عبور یا نام کاربری صحیح نیست')
    context = {
        'login_image': login_image,
    }
    return render(request, 'accounts/login.html',context)



# -----------------------------------------------
@login_required
def customer_register(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'مشتری با موفقیت ثبت شد.')
            return redirect('accounts:customer_register')
        else:
            messages.error(request, 'خطا در ثبت مشتری. لطفاً مجدداً تلاش کنید.')
    else:
        form = CustomerForm()
    return render(request, 'accounts/customer_register.html', {'form': form})









# ------------------------------------------------
@login_required
def customers_with_loans(request):
    query_name = request.GET.get('name', '').strip()
    query_mellicode = request.GET.get('mellicode', '').strip()
    if query_mellicode:
        query_name = ''
    customers_with_loans = Customer.objects.filter(loans__isnull=False).distinct().prefetch_related(
        'loans__guarantees'
    )
    if query_name:
        names = query_name.split()
        if len(names) == 1:
            customers_with_loans = customers_with_loans.filter(
                Q(first_name__icontains=names[0]) | Q(last_name__icontains=names[0])
            )
        elif len(names) >= 2:
            customers_with_loans = customers_with_loans.filter(
                Q(first_name__icontains=names[0]) & Q(last_name__icontains=" ".join(names[1:]))
            )
    if query_mellicode:
        customers_with_loans = customers_with_loans.filter(mellicode__icontains=query_mellicode)
    customers_with_loans_data = []
    for customer in customers_with_loans:
        loans_data = []
        for loan in customer.loans.all():
            guarantees_data = []
            for guarantee in loan.guarantees.all():
                guarantee_info = {
                    "guarantor_name": guarantee.guarantor_name,
                    "guarantee_amount": guarantee.guarantee_amount,
                    "guarantee_type": guarantee.guarantee_type,
                    "guarantee_date": guarantee.guarantee_date,
                }
                guarantees_data.append(guarantee_info)
            loans_data.append(
                {
                    "loan_code": loan.loan_code,
                    "plan": loan.plan,
                    "total_amount": loan.total_amount,
                    "final_amount": loan.final_amount,
                    "loan_date": loan.loan_date,
                    "end_date": loan.end_date,
                    "num_month": loan.num_month,
                    "loan_mande_bedehi": loan.loan_mande_bedehi,
                    "guarantees": guarantees_data,
                }
            )
        customers_with_loans_data.append(
            {
                "id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "mellicode": customer.mellicode,
                "total_loan_amount": customer.total_loan_amount,
                "total_loan_balance": customer.total_loan_balance,
                "loans_count": customer.loans.count(),
                "loans": loans_data,
            })
        print("customers_with_loans_data",customers_with_loans_data)
    context = {
        'customers_with_loans': customers_with_loans_data,
        'query_name': query_name,
        'query_mellicode': query_mellicode,
    }
    return render(request, 'accounts/customers_with_loans.html', context)

