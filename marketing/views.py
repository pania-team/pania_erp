from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import LeadForm
from .models import Lead


@login_required
def lead_list(request):
    leads = Lead.object.all().ordering('created_at')
    return render(request, 'marketing/lead_list.html', {'leads':leads})

# ------------------------------------------
@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk)
    return render(request, 'marketing/lead_detail.html', {'lead':lead})

# ------------------------------------------
@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.post)
        if form.is_valid():
            form.save()
            return redirect('marketing:lead_detail')
        else:
            print('LeadForm errors:', form.errors)
    else:
        form = LeadForm()
        return render(request, 'marketing/lead_form.html', {'form':form})

# ------------------------------------------
@login_required
def lead_update(request, pk):
    lead = get_object_or_404(Lead, pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('marketing:lead_detail')
        else:
            print('LeadForm errors:', form.errors)

    else:
        form = LeadForm(instance=lead)
        return render(request, 'marketing/lead_form.html', {form:form})

# -------------------------------------------
@login_required
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk)
    lead.delete()
    return redirect('marketing:lead_list')

# -------------------------------------------