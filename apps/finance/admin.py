from django.contrib import admin
from django.db import transaction
from apps.finance.models import Transaction, BusinessAsset
import logging

logger = logging.getLogger('custom')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'rial_amount', 'gold_amount', 'create_time')
    list_filter = ('transaction_type', 'create_time')
    search_fields = ('user__username', 'rial_amount', 'gold_amount', )
    date_hierarchy = 'create_time'
    ordering = ('-create_time',)
    readonly_fields = ('create_time',  'rial_amount', 'gold_amount',  'transaction_type')


admin.site.register(Transaction, TransactionAdmin)


class BusinessAssetAdmin(admin.ModelAdmin):
    list_display = ('rial_balance', 'gold_balance')
    readonly_fields = ('rial_balance',  'gold_balance', )



admin.site.register(BusinessAsset, BusinessAssetAdmin)
