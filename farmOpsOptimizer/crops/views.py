from django.shortcuts import render, redirect, get_object_or_404
from .forms import CropForm,  GrazingFieldForm, PlantingFieldForm, PlantingReportForm, HarvestSummaryForm
from .models import Crop, GrazingField, PlantingField, PlantingReport, HarvestSummary
from django.contrib.auth.decorators import login_required
from livestock.models import Herd, Livestock
from resources.models import SeedUsage, FertilizerUsage, PesticideUsage, FeedReport

@login_required
def crops(request):
    crops = Crop.objects.filter(user=request.user)
    return render(request, 'crops/crops.html', {'crops': crops})

@login_required
def fields(request):
    fields = PlantingField.objects.filter(user=request.user)
    return render(request, 'crops/fields.html', {'fields': fields})

@login_required
def add_crop(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.user = request.user  
            crop.save()
            return redirect('crops:crops')
    else:
        form = CropForm()
    return render(request, 'crops/add_crop.html', {'form': form})

@login_required
def add_field(request):
    if request.method == 'POST':
        form = PlantingFieldForm(request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.user = request.user  
            field.save()
            return redirect('crops:fields')  
    else:
        form = PlantingFieldForm()

    return render(request, 'crops/add_field.html', {'form': form})


@login_required
def edit_field(request, field_id):
    field = get_object_or_404(PlantingField, id=field_id)

    if request.method == 'POST':
        form = PlantingFieldForm(request.POST, instance=field)
        if form.is_valid():
            form.save()
            return redirect('crops:fields')  
    else:
        form = PlantingFieldForm(instance=field)

    return render(request, 'crops/edit_field.html', {'form': form, 'field': field})

@login_required
def delete_field(request, field_id):
    field = get_object_or_404(PlantingField, id=field_id)
    if request.user == field.user: 
        field.delete()
  
    return redirect('crops:fields')

@login_required
def edit_crop(request, crop_id): 
    crop = get_object_or_404(Crop, id=crop_id)  

    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('crops:crops') 
    else:
        form = CropForm(instance=crop)

    return render(request, 'crops/edit_crop.html', {'form': form, 'crop': crop})

@login_required
def delete_crop(request, crop_id):
    crop = get_object_or_404(Crop, id=crop_id)
    if request.method == 'POST':
        crop.delete()
        return redirect('crops:crops')   

@login_required
def add_grazing_field(request):
    if request.method == 'POST':
        form = GrazingFieldForm(request.POST)
        if form.is_valid():
            grazing_field = form.save(commit=True)
            grazing_field.user = request.user
            grazing_field.save()
            return redirect('crops:grazing_field_list')  
    else:
        form = GrazingFieldForm()

    return render(request, 'crops/add_grazing_field.html', {'form': form})

@login_required
def grazing_field_list(request):
    grazing_fields = GrazingField.objects.filter(user=request.user)  
    return render(request, 'crops/grazing_field_list.html', {'grazing_fields': grazing_fields})

@login_required
def edit_grazing_field(request, pk):
    field = get_object_or_404(GrazingField, pk=pk)

    if request.method == 'POST':
        form = GrazingFieldForm(request.POST, instance=field)
        if form.is_valid():
            form.save()
            return redirect('crops:grazing_field_list')  
    else:
        form = GrazingFieldForm(instance=field)

    return render(request, 'crops/edit_grazing_field.html', {'form': form, 'field': field})

@login_required
def delete_grazing_field(request, pk):
    field = get_object_or_404(GrazingField, pk=pk)

    if request.method == 'POST':
        field.delete()
    
    return redirect('crops:grazing_field_list')

@login_required
def add_planting_report(request, pk):
    planting_field = get_object_or_404(PlantingField, pk=pk)
    
    if request.method == 'POST':
        form = PlantingReportForm(request.POST)
        if form.is_valid():
            planting_report = form.save(commit=False)
            planting_report.planting_field = planting_field
            planting_report.save()  
            
            return redirect('crops:planting_field_detail', pk=pk)
    else:
        form = PlantingReportForm()
    
    return render(request, 'crops/add_planting_report.html', {'form': form, 'planting_field': planting_field})

@login_required
def planting_field_detail(request, pk):
    planting_field = get_object_or_404(PlantingField, pk=pk)
    planting_reports = planting_field.reports.filter(planting_field=pk, archived=False)
    archived_reports = planting_field.reports.filter(planting_field=pk, archived=True)
    harvest_summaries = HarvestSummary.objects.filter(field=pk)
    seed_usages = SeedUsage.objects.filter(field=pk)
    fertilizer_usages = FertilizerUsage.objects.filter(field=pk)
    pesticide_usages = PesticideUsage.objects.filter(field=pk)
    return render(request, 'crops/planting_field_detail.html', {
        'planting_field': planting_field,
        'planting_reports': planting_reports,
        'archived_reports': archived_reports,
        'harvest_summary': harvest_summaries,
        'seed_usages': seed_usages,
        'fertilizer_usages': fertilizer_usages,
        'pesticide_usages': pesticide_usages,
    })

@login_required
def planting_report_detail(request, pk):
    planting_report = get_object_or_404(PlantingReport, pk=pk)
    return render(request, 'crops/planting_report_detail.html', {'planting_report': planting_report})

@login_required
def archive_all_reports(request, pk):
    planting_field = get_object_or_404(PlantingField, pk=pk)
    planting_field.reports.update(archived=True)
    planting_field.crop = None
    planting_field.planting_date = None
    planting_field.save()
    return redirect('crops:add_harvest_summary', field_id=planting_field.pk)

@login_required
def add_harvest_summary(request, field_id):
    field = get_object_or_404(PlantingField, pk=field_id)
    if request.method == 'POST':
        form = HarvestSummaryForm(request.POST)
        if form.is_valid():
            summary = form.save(commit=False)
            summary.field = field
            summary.save()
            return redirect('crops:planting_field_detail', pk=field.pk)
    else:
        form = HarvestSummaryForm()

    return render(request, 'crops/add_harvest_summary.html', {'form': form, 'field': field})

@login_required
def grazing_field_detail(request, id):
    grazing_field = get_object_or_404(GrazingField, id=id)
    feed_reports = FeedReport.objects.filter(field=id)
    herds = Herd.objects.filter(field=id)
    livestock = Livestock.objects.filter(grazing_field=id)
    
    return render(request, 'crops/grazing_field_detail.html', {
        'grazing_field': grazing_field,
        'herds': herds,
        'livestock': livestock,
        'feed_reports': feed_reports,
    })

@login_required
def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    return render(request, 'crops/crop_detail.html', {'crop': crop})
