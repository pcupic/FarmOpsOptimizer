from django.shortcuts import render, redirect, get_object_or_404
from .forms import EquipmentForm, SeedForm, SeedUsageForm, MaintenanceRecordForm, FertilizerForm, FertilizerUsageForm, PesticideForm, PesticideUsageForm, FeedForm, FeedReportForm
from .models import Equipment, Seed, MaintenanceRecord, Fertilizer, Pesticide, Feed
from crops.models import PlantingField, GrazingField
from django.contrib.auth.decorators import login_required

def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.user = request.user
            equipment.save() 
            return redirect('resources:equipment_list') 
    else:
        form = EquipmentForm()

    return render(request, 'resources/add_equipment.html', {'form': form})


def equipment_list(request):
    equipment = Equipment.objects.filter(user=request.user)
    return render(request, 'resources/equipment_list.html', {'equipment': equipment})

def seed_add(request):
    if request.method == 'POST':
        form = SeedForm(request.POST)
        if form.is_valid():
            seed = form.save(commit=False)
            seed.user = request.user
            seed.save()
            return redirect('resources:seed_list')  
    else:
        form = SeedForm()
    return render(request, 'resources/add_seed.html', {'form': form})

def seed_list(request):
    seeds = Seed.objects.filter(user=request.user)
    return render(request, 'resources/seed_list.html', {'seeds': seeds})

def increase_seed_quantity(request, pk):
    seed = get_object_or_404(Seed, pk=pk)
    seed.quantity = (seed.quantity or 0) + 1
    seed.save()
    return redirect('resources:seed_list')

def decrease_seed_quantity(request, pk):
    seed = get_object_or_404(Seed, pk=pk)
    if seed.quantity and seed.quantity > 0:
        seed.quantity -= 1
        seed.save()
    return redirect('resources:seed_list')

@login_required
def add_seed_usage(request, field_id):
    field = get_object_or_404(PlantingField, id=field_id)
    crop = field.crop

    if request.method == 'POST':
        form = SeedUsageForm(request.POST, crop=crop)
        if form.is_valid():
            seed_usage = form.save(commit=False)
            seed_usage.field = field
            seed_usage.seed = form.cleaned_data['seed']
            seed_usage.save()

            seed_usage.seed.quantity -= form.cleaned_data['quantity_used']
            seed_usage.seed.save()

            return redirect('crops:planting_field_detail', field_id)
    else:
        form = SeedUsageForm(crop=crop)

    return render(request, 'resources/add_seed_usage.html', {'form': form})


def equipment_detail(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    maintenance_records = MaintenanceRecord.objects.filter(equipment=equipment)
    return render(request, 'resources/equipment_detail.html', {'equipment': equipment, 'maintenance_records': maintenance_records})

def add_maintenance_record(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.equipment = equipment
            form.save()
            return redirect('resources:equipment_list')  
    else:
        form = MaintenanceRecordForm()

    return render(request, 'resources/add_maintenance_record.html', {'form': form})

def add_fertilizer(request):
    if request.method == 'POST':
        form = FertilizerForm(request.POST)
        if form.is_valid():
            fertilizer = form.save(commit=False)
            fertilizer.user = request.user
            fertilizer.save()
            return redirect('resources:add_fertilizer')
    else:
        form = FertilizerForm()

    return render(request, 'resources/add_fertilizer.html', {'form': form})

def fertilizer_list(request):
    fertilizers = Fertilizer.objects.filter(user=request.user)
    return render(request, 'resources/fertilizer_list.html', {'fertilizers': fertilizers})

def increase_fertilizer_quantity(request, pk):
    fertilizer = get_object_or_404(Fertilizer, pk=pk)
    fertilizer.quantity = (fertilizer.quantity or 0) + 1
    fertilizer.save()
    return redirect('resources:fertilizer_list')

def decrease_fertilizer_quantity(request, pk):
    fertilizer = get_object_or_404(Fertilizer, pk=pk)
    if fertilizer.quantity and fertilizer.quantity > 0:
        fertilizer.quantity -= 1
        fertilizer.save()
    return redirect('resources:fertilizer_list')
@login_required
def add_fertilizer_usage(request, field_id):
    field = get_object_or_404(PlantingField, id=field_id)

    if request.method == 'POST':
        form = FertilizerUsageForm(request.POST, user=request.user)
        if form.is_valid():
            usage = form.save(commit=False)
            fertilizer = usage.fertilizer
            amount_used = usage.amount_used

            if amount_used > fertilizer.quantity:
                form.add_error('amount_used', 'You cannot use more fertilizer than is available in stock.')
                return render(request, 'resources/add_fertilizer_usage.html', {
                    'form': form,
                    'field': field,
                })

            usage.field = field
            usage.save()

            fertilizer.quantity -= amount_used
            fertilizer.save()

            return redirect('crops:planting_field_detail', field_id)
    else:
        form = FertilizerUsageForm(user=request.user)

    return render(request, 'resources/add_fertilizer_usage.html', {
        'form': form,
        'field': field,
    })



    
def add_pesticide(request):
    if request.method == 'POST':
        form = PesticideForm(request.POST)
        if form.is_valid():
            pesticide = form.save(commit=False)
            pesticide.user = request.user
            pesticide.save()
            return redirect('resources:pesticide_list')  
    else:
        form = PesticideForm()

    return render(request, 'resources/add_pesticide.html', {'form': form})

def pesticide_list(request):
    pesticides = Pesticide.objects.filter(user=request.user)
    
    return render(request, 'resources/pesticide_list.html', {'pesticides': pesticides})


def increase_quantity_pesticide(request, pesticide_id):
    pesticide = get_object_or_404(Pesticide, id=pesticide_id)
    pesticide.quantity += 1 
    pesticide.save()
    return redirect('resources:pesticide_list')

def decrease_quantity_pesticide(request, pesticide_id):
    pesticide = get_object_or_404(Pesticide, id=pesticide_id)
    if pesticide.quantity > 0:
        pesticide.quantity -= 1  
        pesticide.save()
    return redirect('resources:pesticide_list')

@login_required
def add_pesticide_usage(request, field_id):
    field = get_object_or_404(PlantingField, id=field_id)

    if request.method == 'POST':
        form = PesticideUsageForm(request.POST, user=request.user)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.field = field
            usage.save()

            usage.pesticide.quantity -= usage.quantity_used
            usage.pesticide.save()

            return redirect('crops:planting_field_detail', field_id)
    else:
        form = PesticideUsageForm(user=request.user)

    return render(request, 'resources/add_pesticide_usage.html', {
        'form': form,
        'field': field,
    })
    
    
def add_feed(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.user = request.user
            feed.save()
            return redirect('resources:feed_list')  
    else:
        form = FeedForm()

    return render(request, 'resources/add_feed.html', {'form': form})

def feed_list(request):
    feeds = Feed.objects.filter(user=request.user)
    
    return render(request, 'resources/feed_list.html', {'feeds': feeds})

def increase_quantity(request, feed_id):
    feed = Feed.objects.get(id=feed_id)
    feed.quantity += 1  
    feed.save()
    return redirect('resources:feed_list')

def decrease_quantity(request, feed_id):
    feed = Feed.objects.get(id=feed_id)
    if feed.quantity > 0:
        feed.quantity -= 1  
        feed.save()
    return redirect('resources:feed_list')

def add_feed_report(request, pk):
    grazing_field = get_object_or_404(GrazingField, pk=pk)

    if request.method == 'POST':
        form = FeedReportForm(request.POST)
        if form.is_valid():
            feed = form.cleaned_data['feed']
            quantity_used = form.cleaned_data['quantity_used']

            if quantity_used > feed.quantity:
                form.add_error('quantity_used', f"Cannot use more than {feed.quantity} {feed.get_unit_of_measure_display()}.")
            else:
                feed_report = form.save(commit=False)
                feed_report.field = grazing_field
                feed_report.save()

                feed.quantity -= quantity_used
                feed.save()

                return redirect('crops:grazing_field_detail', pk)
    else:
        form = FeedReportForm()

    return render(request, 'resources/add_feed_report.html', {
        'form': form,
        'grazing_field': grazing_field, 
    })

def edit_equipment(request, id):
    equipment = get_object_or_404(Equipment, id=id)  
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)  
        if form.is_valid():
            form.save()  
            return redirect('resources:equipment_detail', id) 
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'resources/edit_equipment.html', {'form': form, 'equipment': equipment})

def delete_equipment(request, id):
    equipment = get_object_or_404(Equipment, id=id)  
    if request.method == 'POST':
        equipment.delete() 
        return redirect('resources:equipment_list') 
    

def edit_seed(request, pk):
    seed = get_object_or_404(Seed, pk=pk)
    if request.method == "POST":
        form = SeedForm(request.POST, instance=seed)
        if form.is_valid():
            form.save()
            return redirect('resources:seed_list')  
    else:
        form = SeedForm(instance=seed)
    return render(request, 'resources/edit_seed.html', {'form': form, 'seed': seed})

def delete_seed(request, pk):
    seed = get_object_or_404(Seed, pk=pk)
    
    if request.method == "POST":
        seed.delete()   
    return redirect('resources:seed_list') 

def edit_fertilizer(request, id):
    fertilizer = get_object_or_404(Fertilizer, id=id)
    
    if request.method == 'POST':
        form = FertilizerForm(request.POST, instance=fertilizer)
        if form.is_valid():
            form.save()
            return redirect('resources:fertilizer_list')  
    else:
        form = FertilizerForm(instance=fertilizer) 
    
    return render(request, 'resources/edit_fertilizer.html', {'form': form, 'fertilizer': fertilizer})

def delete_fertilizer(request, id):
    fertilizer = get_object_or_404(Fertilizer, id=id)

    if request.method == 'POST':
        fertilizer.delete()
    return redirect('resources:fertilizer_list') 

def edit_pesticide(request, id):
    pesticide = get_object_or_404(Pesticide, id=id)

    if request.method == 'POST':
        form = PesticideForm(request.POST, instance=pesticide)
        if form.is_valid():
            form.save()
            return redirect('resources:pesticide_list')  
    else:
        form = PesticideForm(instance=pesticide) 

    return render(request, 'resources/edit_pesticide.html', {'form': form, 'pesticide': pesticide})

def delete_pesticide(request, id):
    pesticide = get_object_or_404(Pesticide, id=id)

    if request.method == 'POST':
        pesticide.delete()
    return redirect('resources:pesticide_list')  
    
def edit_feed(request, id):
    feed = get_object_or_404(Feed, id=id)

    if request.method == 'POST':
        form = FeedForm(request.POST, instance=feed)
        if form.is_valid():
            form.save()
            return redirect('resources:feed_list')
    else:
        form = FeedForm(instance=feed)

    return render(request, 'edit_feed.html', {'form': form})

def delete_feed(request, id):
    feed = get_object_or_404(Feed, id=id)

    if request.method == 'POST':
        feed.delete()
    return redirect('resources:feed_list')


