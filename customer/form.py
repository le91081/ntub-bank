from django import forms
from .models import Customer, CustomerImage


class CustomerForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Customer
        # fields = '__all__'
        

class UploadImageForm(forms.Form):
    file = forms.FileField()
    type = forms.ChoiceField(choices=CustomerImage.TYPE_CHOICES)