from django import forms 
from .models import IdLiquidacion

class BuscarIdLiquidacionForm(forms.Form):
    periodo = forms.ChoiceField(choices=[('', 'TODOS'), ] + IdLiquidacion.Meses.choices, required=False)
    anio = forms.IntegerField(required=False, label='Año')