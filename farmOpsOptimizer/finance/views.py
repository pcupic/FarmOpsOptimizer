from decimal import Decimal
from django.shortcuts import render
from django.db.models import Sum
from resources.models import Seed, Fertilizer, Equipment
from livestock.models import Livestock
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, DecimalField
from crops.models import PlantingField
from resources.models import Feed, Pesticide, Equipment, Fertilizer, FertilizerUsage, SeedUsage, PesticideUsage
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.http import JsonResponse
from .models import DailyBalance
from django.utils import timezone

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
    livestocks = Livestock.objects.filter(user=request.user)
    livestock_data = []

    for livestock in livestocks:
        health_records = livestock.health_records.all()
        health_costs = [hr.cost_of_treatment or 0 for hr in health_records]
        health_total = sum(health_costs)

        vaccination_records = livestock.vaccination_records.all()
        vaccine_costs = [vr.cost_of_vaccine or 0 for vr in vaccination_records]
        vaccine_total = sum(vaccine_costs)

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
    
    equipment = Equipment.objects.filter(user=user).annotate(
        total_maintenance_cost=Coalesce(
            Sum('maintenance_records__cost'),
            Value(0, output_field=DecimalField())
        )
    )
    
    equipment_with_maintenance = []
    for eq in equipment:
        equipment_with_maintenance.append({
            'object': eq, 
            'maintenance_records': eq.maintenance_records.all()
        })

    seeds = Seed.objects.filter(user=user)
    fertilizers = Fertilizer.objects.filter(user=user)
    pesticides = Pesticide.objects.filter(user=user)
    feeds = Feed.objects.filter(user=user)

    context = {
        'equipment': equipment_with_maintenance,  
        'seeds': seeds,
        'fertilizers': fertilizers,
        'pesticides': pesticides,
        'feeds': feeds,
        'totals': {
            'equipment': get_total_value_only(equipment),  
            'seeds': get_total_price_quantity(seeds),
            'fertilizers': get_total_price_quantity(fertilizers),
            'pesticides': get_total_price_quantity(pesticides),
            'feeds': get_total_price_quantity(feeds),
        }
    }
    return render(request, 'resource_assets.html', context)

def calculate_balance(user):
    planting_fields = PlantingField.objects.filter(user=user)
    total_crop_costs = Decimal(0)
    total_crop_revenue = Decimal(0)

    for field in planting_fields:
        for summary in field.harvest_summaries.all():
            total_crop_revenue += Decimal(summary.total_revenue or 0)

        for usage in SeedUsage.objects.filter(field=field):
            if usage.seed and usage.seed.price_per_unit is not None:
                total_crop_costs += Decimal(usage.quantity_used) * usage.seed.price_per_unit

        for usage in FertilizerUsage.objects.filter(field=field):
            if usage.fertilizer and usage.fertilizer.price_per_unit is not None:
                total_crop_costs += Decimal(usage.amount_used) * usage.fertilizer.price_per_unit

        for usage in PesticideUsage.objects.filter(field=field):
            if usage.pesticide and usage.pesticide.price_per_unit is not None:
                total_crop_costs += Decimal(usage.quantity_used) * usage.pesticide.price_per_unit

    livestocks = Livestock.objects.filter(user=user)
    total_livestock_costs = Decimal(0)

    for livestock in livestocks:
        total_livestock_costs += sum(Decimal(hr.cost_of_treatment or 0) for hr in livestock.health_records.all())
        total_livestock_costs += sum(Decimal(vr.cost_of_vaccine or 0) for vr in livestock.vaccination_records.all())

    equipment = Equipment.objects.filter(user=user).annotate(
        total_maintenance_cost=Coalesce(
            Sum('maintenance_records__cost'),
            Value(0, output_field=DecimalField())
        )
    )
    total_equipment_costs = sum(eq.total_maintenance_cost for eq in equipment)

    _, seed_value = get_total_price_quantity(Seed.objects.filter(user=user))
    _, fertilizer_value = get_total_price_quantity(Fertilizer.objects.filter(user=user))
    _, pesticide_value = get_total_price_quantity(Pesticide.objects.filter(user=user))
    _, feed_value = get_total_price_quantity(Feed.objects.filter(user=user))

    resource_total_cost = seed_value + fertilizer_value + pesticide_value + feed_value

    total_expenses = (
        total_crop_costs +
        total_livestock_costs +
        total_equipment_costs +
        resource_total_cost
    )
    total_income = total_crop_revenue

    balance = total_income - total_expenses
    return {
        'income': total_income,
        'expenses': total_expenses,
        'balance': balance
    }


@login_required
def financial_balance(request):
    balance_data = calculate_balance(request.user)
    
    today = timezone.now().date()

    DailyBalance.objects.update_or_create(
        user=request.user,
        date=today,
        defaults={
            'income': balance_data['income'],
            'expenses': balance_data['expenses'],
            'balance': balance_data['balance']
        }
    )

    return render(request, 'financial_balance.html', {
        'balance': balance_data
    })

@login_required
def balance_chart_data(request):
    data = DailyBalance.objects.filter(user=request.user).order_by('date')
    return JsonResponse({
        'labels': [entry.date.strftime('%d.%m.') for entry in data],
        'income': [float(entry.income) for entry in data],
        'expenses': [float(entry.expenses) for entry in data],
        'balance': [float(entry.balance) for entry in data],
    })

