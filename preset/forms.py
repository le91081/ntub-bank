from django import forms
from .models import Preset


class PresetForm(forms.ModelForm):

    class Meta:
        model = Preset
        fields = '__all__'
