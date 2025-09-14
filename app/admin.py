from django.contrib import admin
from import_export.admin import ExportMixin
from app.models.order_models import Order  
from app.models.transaction_models import Transaction  # Adjust the import path to match your structure
from app.models.wallet_models import Wallet 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(Order)
class OrderAdmin(ExportMixin, admin.ModelAdmin):
    list_display = [
        'user', 'service', 'country', 'number', 'code', 'cost', 'transaction',
        'status', 'created_at', 'updated_at'
    ]
    search_fields = ['user__email', 'user__username', 'service', 'country', 'transaction__reference']
    list_filter = ['status', 'user','service', 'country', 'created_at', 'updated_at']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']




@admin.register(Transaction)
class TransactionAdmin(ExportMixin, admin.ModelAdmin):
    list_display = [
        'user', 'wallet', 'type', 'status', 'amount',
        'receipt_id', 'reference', 'created_at', 'updated_at'
    ]
    search_fields = ['receipt_id', 'reference', 'description']
    list_filter = ['type', 'status', 'created_at', 'updated_at']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']



@admin.register(Wallet)
class WalletAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['user', 'wallet_id', 'balance', 'created_at', 'updated_at']
    search_fields = ['user__email', 'wallet_id']
    list_filter = ['created_at', 'updated_at']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
