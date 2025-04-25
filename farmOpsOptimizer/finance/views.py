from decimal import Decimal
from django.shortcuts import render
from django.db.models import Sum, F
from resources.models import Seed, Fertilizer, Equipment
from livestock.models import GrazingField, Livestock, Herd
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from crops.models import PlantingField, HarvestSummary, Crop
from resources.models import Feed, Pesticide, Equipment, Fertilizer, FertilizerUsage, SeedUsage, PesticideUsage
from django.db.models.functions import Coalesce
from django.db.models import Value

@login_required
def planting_field_overview(request):
    planting_fields = PlantingField.objects.filter(user=request.user)

    fields_data = []

    for field in planting_fields:
        harvest_summaries = field.harvest_summaries.all()

        total_revenue = sum(summary.total_revenue or 0 for summary in harvest_summaries)

        seed_usages = SeedUsage.objects.filter(field=field)
        fertilizer_usages = FertilizerUsage.objects.filter(field=field)
        pesticide_usages = PesticideUsage.objects.filter(field=field)

        total_seed_cost = sum(
            Decimal(seed_usage.quantity_used) * seed_usage.seed.price_per_unit
            for seed_usage in seed_usages if seed_usage.seed.price_per_unit is not None
        )

        total_fertilizer_cost = sum(
            Decimal(fertilizer_usage.amount_used) * fertilizer_usage.fertilizer.price_per_unit
            for fertilizer_usage in fertilizer_usages if fertilizer_usage.fertilizer.price_per_unit is not None
        )

        total_pesticide_cost = sum(
            Decimal(pesticide_usage.quantity_used) * pesticide_usage.pesticide.price_per_unit
            for pesticide_usage in pesticide_usages if pesticide_usage.pesticide.price_per_unit is not None
        )
        
        net_profit_loss = total_revenue - (total_seed_cost + total_fertilizer_cost + total_pesticide_cost)

        fields_data.append({
            'field': field,
            'harvest_summaries': harvest_summaries,
            'net_profit_loss': net_profit_loss,
            'seed_usages': seed_usages,
            'fertilizer_usages': fertilizer_usages,
            'pesticide_usages': pesticide_usages,
            'total_seed_cost': total_seed_cost,
            'total_fertilizer_cost': total_fertilizer_cost,
            'total_pesticide_cost': total_pesticide_cost,
        })

    return render(request, 'planting_field_overview.html', {
        'fields_data': fields_data,
    })
    
def livestock_costs(request):
    # Pronađi sve livestocke za trenutnog korisnika
    livestocks = Livestock.objects.filter(user=request.user)
    livestock_data = []

    for livestock in livestocks:
        # Troškovi health recorda
        health_records = livestock.health_records.all()
        health_costs = [hr.cost_of_treatment or 0 for hr in health_records]
        health_total = sum(health_costs)

        # Troškovi vakcina
        vaccination_records = livestock.vaccination_records.all()
        vaccine_costs = [vr.cost_of_vaccine or 0 for vr in vaccination_records]
        vaccine_total = sum(vaccine_costs)

        # Ukupno
        total = health_total + vaccine_total

        livestock_data.append({
            'livestock': livestock,
            'health_records': health_records,
            'health_costs': health_costs,
            'health_total': health_total,
            'vaccination_records': vaccination_records,
            'vaccine_costs': vaccine_costs,
            'vaccine_total': vaccine_total,
            'total': total,
        })

    return render(request, 'livestock_costs.html', {'livestock_data': livestock_data})


def get_total_price_quantity(queryset, quantity_field='quantity', price_field='price_per_unit'):
    total_quantity = sum(Decimal(str(getattr(item, quantity_field) or 0)) for item in queryset)
    total_value = sum(
        Decimal(str(getattr(item, quantity_field) or 0)) *
        Decimal(str(getattr(item, price_field) or 0)) for item in queryset
    )
    return total_quantity, total_value

def get_total_value_only(queryset, value_field='value'):
    total_value = sum(Decimal(str(getattr(item, value_field) or 0)) for item in queryset)
    return None, total_value

def resource_assets(request):
    user = request.user
    
    # Annotiraj opremu s ukupnim troškovima održavanja
    equipment = Equipment.objects.filter(user=user).annotate(
        total_maintenance_cost=Coalesce(
            Sum('maintenance_records__cost'),
            Value(0, output_field=DecimalField())
        )
    )
    
    # Dodaj maintenance records za svaku opremu
    equipment_with_maintenance = []
    for eq in equipment:
        equipment_with_maintenance.append({
            'object': eq,  # Annotirani objekt s ukupnim troškovima
            'maintenance_records': eq.maintenance_records.all()
        })

    # Ostali resursi
    seeds = Seed.objects.filter(user=user)
    fertilizers = Fertilizer.objects.filter(user=user)
    pesticides = Pesticide.objects.filter(user=user)
    feeds = Feed.objects.filter(user=user)

    context = {
        'equipment': equipment_with_maintenance,  # Kombinirani podaci
        'seeds': seeds,
        'fertilizers': fertilizers,
        'pesticides': pesticides,
        'feeds': feeds,
        'totals': {
            'equipment': get_total_value_only(equipment),  # Annotirani queryset
            'seeds': get_total_price_quantity(seeds),
            'fertilizers': get_total_price_quantity(fertilizers),
            'pesticides': get_total_price_quantity(pesticides),
            'feeds': get_total_price_quantity(feeds),
        }
    }
    return render(request, 'resource_assets.html', context)


