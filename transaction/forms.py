from django import forms
from .models import TransactionRecord


class TransactionRecordForm(forms.ModelForm):
    #usage = forms.CharField(label='資金用途', widget=forms.Textarea)

    class Meta:
        model = TransactionRecord
        #fields = '__all__'
        fields = ['amount', 'operation', 'from_account',
                  'to_account', 'payer', 'user', 'date', 'funds', 'usage']
