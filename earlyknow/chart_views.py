from random import shuffle

from chartjs.colors import next_color, COLORS
from chartjs.views.lines import BaseLineChartView

from .views import TransactionRecordFilter


class ColorLineChartView(BaseLineChartView):
    def get_colors(self):
            colors = COLORS[:]
            shuffle(colors)
            return next_color(colors)


class AccountAmountChartJSONView(ColorLineChartView):
    account_amount_warnings = TransactionRecordFilter.account_amount_warnings

    def get_labels(self):
        labels = []
        [labels.append(warning['to_account__customer_id__name']) for warning in self.account_amount_warnings]
        return labels

    def get_providers(self):
        return ['金額']

    def get_data(self):
        datasets = []
        [datasets.append(warning['account_amount']) for warning in self.account_amount_warnings]
        return [datasets]


class AccountCountChartJSONView(ColorLineChartView):
    account_count_warnings = TransactionRecordFilter.account_count_warnings

    def get_labels(self):
        labels = []
        [labels.append(warning['to_account__customer_id__name']) for warning in self.account_count_warnings]
        return labels

    def get_providers(self):
        return ['次數']

    def get_data(self):
        datasets = []
        [datasets.append(warning['account_count']) for warning in self.account_count_warnings]
        return [datasets]


class AddressAmountChartJSONView(ColorLineChartView):
    address_amount_warnings = TransactionRecordFilter.address_amount_warnings

    def get_labels(self):
        labels = []
        [labels.append(warning['to_account__customer_id__address']) for warning in self.address_amount_warnings]
        return labels

    def get_providers(self):
        return ['金額']

    def get_data(self):
        datasets = []
        [datasets.append(warning['address_amount']) for warning in self.address_amount_warnings]
        return [datasets]


class AddressCountChartJSONView(ColorLineChartView):
    address_count_warnings = TransactionRecordFilter.address_count_warnings

    def get_labels(self):
        labels = []
        [labels.append(warning['to_account__customer_id__address']) for warning in self.address_count_warnings]
        return labels

    def get_providers(self):
        return ['次數']

    def get_data(self):
        datasets = []
        [datasets.append(warning['address_count']) for warning in self.address_count_warnings]
        return [datasets]

class DaysTransactionRecordChartJSONView(ColorLineChartView):
    days_transation_record = TransactionRecordFilter.days_transation_record

    def get_labels(self):
        labels = []
        [labels.append(warning['date_date']) for warning in self.days_transation_record]
        return labels

    def get_providers(self):
        return ['金額']

    def get_data(self):
        datasets = []
        [datasets.append(warning['sum_amount']) for warning in self.days_transation_record]
        return [datasets]


class Top10TransactionRecordChartJSONView(ColorLineChartView):
    top10_transation_record = TransactionRecordFilter.top10_transation_record

    def get_labels(self):
        labels = []
        [labels.append(warning['to_account__customer_id__name']) for warning in self.top10_transation_record]
        return labels

    def get_providers(self):
        return ['金額']

    def get_data(self):
        datasets = []
        [datasets.append(warning['sum_amount']) for warning in self.top10_transation_record]
        return [datasets]


account_amount_chart_json = AccountAmountChartJSONView.as_view()
account_count_chart_json = AccountCountChartJSONView.as_view()
address_amount_chart_json = AddressAmountChartJSONView.as_view()
address_count_chart_json = AddressCountChartJSONView.as_view()
days_transation_record_chart_json = DaysTransactionRecordChartJSONView.as_view()
top10_transation_record_chart_json = Top10TransactionRecordChartJSONView.as_view()
