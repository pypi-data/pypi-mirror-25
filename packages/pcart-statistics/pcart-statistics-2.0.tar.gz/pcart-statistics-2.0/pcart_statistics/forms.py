from django import forms
from .models import LastVisitedPluginModel


class LastVisitedPluginForm(forms.ModelForm):
    model = LastVisitedPluginModel

    class Meta:
        fields = '__all__'
