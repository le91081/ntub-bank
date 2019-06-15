from decimal import Decimal
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate

from transaction.models import TransactionRecord

# Create your views here.


class TransactionRecordFilter:
    start_date = datetime.datetime.now() + datetime.timedelta(days=-30)
    end_date = datetime.datetime.now()

    month_transation_record = TransactionRecord.objects\
        .filter(operation=1)\
        .filter(date__range=(start_date, end_date))

    account_amount_warnings = month_transation_record\
        .values('to_account__customer_id__name')\
        .annotate(account_amount=Sum('amount'))\
        .filter(account_amount__gt=Decimal('1000000'))\
        .order_by('-account_amount')

    account_count_warnings = month_transation_record\
        .values('to_account__customer_id__name')\
        .annotate(account_count=Count('to_account'))\
        .filter(account_count__gt=10)\
        .order_by('-account_count')

    address_amount_warnings = month_transation_record\
        .values('to_account__customer_id__address')\
        .annotate(address_amount=Sum('amount'))\
        .filter(address_amount__gt=Decimal('1000000'))\
        .order_by('-address_amount')

    address_count_warnings = month_transation_record\
        .values('to_account__customer_id__address')\
        .annotate(address_count=Count('to_account'))\
        .filter(address_count__gt=10)\
        .order_by('-address_count')

    days_transation_record = month_transation_record\
        .annotate(date_date=TruncDate('date'))\
        .values('date_date')\
        .annotate(sum_amount=Sum('amount'))\
        .order_by('-date_date')[0:7]

    top10_transation_record = month_transation_record\
        .values('to_account__customer_id__name')\
        .annotate(sum_amount=Sum('amount'))\
        .order_by('-sum_amount')[:10]


@login_required
def index(request):
    account_amount_warnings = TransactionRecordFilter.account_amount_warnings
    account_count_warnings = TransactionRecordFilter.account_count_warnings
    address_amount_warnings = TransactionRecordFilter.address_amount_warnings
    address_count_warnings = TransactionRecordFilter.address_count_warnings
    days_transation_record = TransactionRecordFilter.days_transation_record
    top10_transation_record = TransactionRecordFilter.top10_transation_record

    return render(request, 'earlyknow/index.html', {
        'account_amount_warnings': account_amount_warnings,
        'account_count_warnings': account_count_warnings,
        'address_amount_warnings': address_amount_warnings,
        'address_count_warnings': address_count_warnings,
        'days_transation_record': days_transation_record,
        'top10_transation_record': top10_transation_record
    })
