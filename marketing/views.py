from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import LeadForm, ProductForm
from .models import Lead, Product, Tag


@login_required
def lead_list(request):
    leads = Lead.objects.all().order_by('created_at')
    return render(request, 'marketing/lead_list.html', {'leads':leads})

# ------------------------------------------
@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'marketing/lead_detail.html', {'lead': lead})

# ------------------------------------------
@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('marketing:lead_list')
        else:
            print('LeadForm errors:', form.errors)
    else:
        form = LeadForm()
        return render(request, 'marketing/lead_create.html', {'form':form})

# ------------------------------------------
@login_required
def lead_update(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('marketing:lead_detail', pk=lead.pk)
        else:
            print('LeadForm errors:', form.errors)
    else:
        form = LeadForm(instance=lead)
    return render(request, 'marketing/lead_create.html', {'form': form})

# -------------------------------------------
@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    return redirect('marketing:lead_list')

# -------------------------------------------

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'product': {
                        'id': product.id,
                        'text': str(product)
                    }
                })
            return redirect('marketing:lead_list')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': form.errors
                })
            print('ProductForm errors:', form.errors)
    else:
        form = ProductForm()
    return render(request, 'marketing/product_create.html', {'form': form})

def tag_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            try:
                tag = Tag.objects.create(name=name)
                return JsonResponse({
                    'success': True,
                    'tag': {
                        'id': tag.id,
                        'text': tag.name
                    }
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
        return JsonResponse({
            'success': False,
            'error': 'نام تگ الزامی است'
        })
    return JsonResponse({
        'success': False,
        'error': 'متد درخواست نامعتبر است'
    })