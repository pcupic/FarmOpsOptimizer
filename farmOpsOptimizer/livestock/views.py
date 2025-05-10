from django.shortcuts import render, redirect, get_object_or_404
from .forms import LivestockForm, HealthRecordForm, VaccinationRecordForm, SpeciesForm, HerdForm
from .models import Livestock, Species, Herd, HealthRecord, VaccinationRecord
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def add_livestock(request):
    if request.method == 'POST':
        form = LivestockForm(request.POST, user=request.user)
        if form.is_valid():
            livestock = form.save(commit=False) 
            livestock.user = request.user 
            livestock.save()  
            return redirect('livestock:livestock_list')
    else:
        form = LivestockForm(user=request.user)
    return render(request, 'livestock/add_livestock.html', {'form': form})

@login_required
def livestock_list(request):
    livestock = Livestock.objects.filter(user=request.user)
    return render(request, 'livestock/livestock_list.html', {'livestock': livestock})

@login_required
def species_list(request):
    species = Species.objects.filter(status='approved')
    return render(request, 'livestock/species_list.html', {'species': species})

@login_required
def species_add(request):
    if request.method == 'POST':
        form = SpeciesForm(request.POST)
        if form.is_valid():
            species = form.save(commit=False)
            if request.user.is_staff or request.user.is_superuser:
                species.status = 'approved'
            else:
                species.status = 'pending'
            species.created_by = request.user
            species.save()
            return redirect('livestock:species_list')  
    else:
        form = SpeciesForm()
    return render(request, 'livestock/add_species.html', {'form': form})


@login_required
def species_detail(request, pk):
    species = get_object_or_404(Species, pk=pk)
    return render(request, 'livestock/species_detail.html', {'species': species})

@login_required
def livestock_detail(request, id):
    livestock = get_object_or_404(Livestock, id=id)
    
    latest_health_record = livestock.health_records.order_by('-date_recorded').first()

    return render(request, 'livestock/livestock_detail.html', {'livestock': livestock, 'latest_health_record': latest_health_record})

@login_required
def herd_list(request):
    herds = Herd.objects.filter(user=request.user)
    return render(request, 'livestock/herd_list.html', {'herds': herds})

@login_required
def add_herd(request):
    if request.method == 'POST':
        form = HerdForm(request.POST)
        if form.is_valid():
            herd = form.save(commit=False) 
            herd.user = request.user 
            herd.save()  
            return redirect('livestock:herd_list')
    else:
        form = HerdForm()
    return render(request, 'livestock/add_herd.html', {'form': form})

@login_required
def herd_detail(request, pk):
    herd = get_object_or_404(Herd, pk=pk)
    livestock = herd.livestock.all()
    return render(request, 'livestock/herd_detail.html', {'herd': herd, 'livestock': livestock})

@login_required
def add_livestock_to_herd(request, herd_id):
    herd = get_object_or_404(Herd, id=herd_id, user=request.user)
    available_livestock = Livestock.objects.filter(herd__isnull=True, species=herd.species, user=request.user)

    if request.method == 'POST':
        selected_ids = request.POST.getlist('livestock')
        Livestock.objects.filter(id__in=selected_ids).update(herd=herd)
        return redirect('livestock:herd_detail', herd.id)

    return render(request, 'livestock/add_livestock_to_herd.html', {
        'herd': herd,
        'available_livestock': available_livestock,
    })
    
@login_required
def add_health_record(request, pk):
    livestock = get_object_or_404(Livestock, pk=pk)

    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.livestock = livestock
            record.save()
            return redirect('livestock:livestock_detail', id=pk)
    else:
        form = HealthRecordForm()

    return render(request, 'livestock/add_health_record.html', {'form': form, 'livestock': livestock})

@login_required
def add_vaccination_record(request, pk):
    livestock = get_object_or_404(Livestock, pk=pk)

    if request.method == 'POST':
        form = VaccinationRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.livestock = livestock
            record.save()
            return redirect('livestock:livestock_detail', id=pk)
    else:
        form = VaccinationRecordForm()

    return render(request, 'livestock/add_vaccination_record.html', {'form': form, 'livestock': livestock})

@login_required
@staff_member_required
def pending_species_list(request):
    species = Species.objects.filter(status='pending')  
    return render(request, 'livestock/pending_species_list.html', {'species': species})

@login_required
@staff_member_required
def approve_species(request, pk):
    if request.method == 'POST':
        species = get_object_or_404(Species, pk=pk)
        species.status = 'approved'
        species.save()
    return redirect('livestock:pending_species_list')

@login_required
@staff_member_required
def delete_species(request, pk):
    if request.method == 'POST':
        species = get_object_or_404(Species, pk=pk)
        species.delete()
    return redirect('livestock:pending_species_list')

@login_required
def health_record_detail(request, id):
    health_record = get_object_or_404(HealthRecord, id=id)

    return render(request, 'livestock/health_record_detail.html', {'health_record': health_record})

@login_required
def vaccination_detail(request, id):
    vaccination = get_object_or_404(VaccinationRecord, id=id)
    
    return render(request, 'livestock/vaccination_detail.html', {'vaccination': vaccination})

@login_required
def edit_livestock(request, pk):
    livestock = get_object_or_404(Livestock, pk=pk)
    
    if request.method == 'POST':
        form = LivestockForm(request.POST, instance=livestock)
        if form.is_valid():
            form.save()
            return redirect('livestock:livestock_list') 
    else:
        form = LivestockForm(instance=livestock)

    return render(request, 'livestock/edit_livestock.html', {'form': form, 'livestock': livestock})

@login_required
def delete_livestock(request, pk):
    livestock = get_object_or_404(Livestock, pk=pk)

    if request.method == 'POST':
        livestock.delete()
    return redirect('livestock:livestock_list')  

