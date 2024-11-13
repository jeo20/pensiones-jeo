from django import forms 
from apps.app_id_liquidacion.models import IdLiquidacion
from apps.app_ubicacion.models import Ubicacion


## TODO
## formulario para selección de la liquidación (abierta)
## Genera la liquidación, usando la view generar_detalle_liquidacion

class BusquedaReciboLiquidacionForm(forms.Form):
    idliq = forms.ModelChoiceField(queryset=IdLiquidacion.objects.all(), label='Seleccione Liquidación')
    idubicacion = forms.ModelChoiceField(queryset=Ubicacion.objects.all(), label='Seleccione Ubicación') 
    idlegajo = forms.IntegerField(label='Número de Legajo')

