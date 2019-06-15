from django.urls import path
from . import views, chart_views

app_name = 'earlyknow'
urlpatterns = [
    path('', views.index, name='index'),

    path('account_amount_chart_json/', chart_views.account_amount_chart_json, name='account_amount_chart_json'),
    path('account_count_chart_json/', chart_views.account_count_chart_json, name='account_count_chart_json'),
    path('address_amount_chart_json/', chart_views.address_amount_chart_json, name='address_amount_chart_json'),
    path('address_count_chart_json/', chart_views.address_count_chart_json, name='address_count_chart_json'),
    path('days_transation_record_chart_json/', chart_views.days_transation_record_chart_json, name='days_transation_record_chart_json'),
    path('top10_transation_record_chart_json/', chart_views.top10_transation_record_chart_json, name='top10_transation_record_chart_json'),
]
