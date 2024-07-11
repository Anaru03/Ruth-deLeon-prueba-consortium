from django.contrib import admin
from .models import Spending

@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'created_at', 'type', 'status')
    list_filter = ('created_at', 'status')
    search_fields = ('description',)

    def created_by(self, obj):
        return obj.created_by.username

    created_by.admin_order_field = 'created_by' 
