from django.contrib import admin

from spending_control.models import Spending


class LiquidationInline(admin.TabularInline):
    model = Spending.liquidations.through
    extra = 1

@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'amount', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('description', 'amount')
    inlines = (LiquidationInline,)