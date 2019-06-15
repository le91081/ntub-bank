from django import forms
from .models import TransactionRecord


class TransactionRecordForm(forms.ModelForm):

    class Meta:
        model = TransactionRecord
        fields = '__all__'