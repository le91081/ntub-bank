from django.contrib import admin
from .models import TransactionRecord, Payer


admin.site.register(TransactionRecord)
admin.site.register(Payer)
