from decimal import Decimal
from django.shortcuts import render
from django.db.models import Sum, DecimalField, Value
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from resources.models import Seed, Fertilizer, Equipment, Feed, Pesticide, FertilizerUsage, SeedUsage, PesticideUsage
from livestock.models import Livestock
from crops.models import PlantingField
from .models import DailyBalance

from .utils import get_total_price_quantity, get_total_value_only, calculate_balance

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

    return render(request, 'finance/planting_field_overview.html', {
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

    return render(request, 'finance/livestock_costs.html', {'livestock_data': livestock_data})

def resource_assets(request):
    user = request.user
    equipment = Equipment.objects.filter(user=user).annotate(
        total_maintenance_cost=Coalesce(
            Sum('maintenance_records__cost'),
            Value(0, output_field=DecimalField())
        )
    )
    equipment_with_maintenance = [
        {'object': eq, 'maintenance_records': eq.maintenance_records.all()}
        for eq in equipment
    ]

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
    return render(request, 'finance/resource_assets.html', context)

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

    return render(request, 'finance/financial_balance.html', {
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
