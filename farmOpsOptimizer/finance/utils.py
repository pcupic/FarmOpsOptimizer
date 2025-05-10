from resources.models import Fertilizer, Seed, Pesticide, PesticideUsage, FertilizerUsage, SeedUsage, Equipment, Feed
from decimal import Decimal
from django.db.models.functions import Coalesce
from django.db.models import Sum, Value, DecimalField
from crops.models import PlantingField
from livestock.models import Livestock

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
