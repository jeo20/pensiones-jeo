from django import forms 
from apps.app_id_liquidacion.models import IdLiquidacion
from apps.app_ubicacion.models import Ubicacion


class MovMesForm(forms.Form):
    id_liquidacion = forms.ModelChoiceField(queryset=IdLiquidacion.objects.filter(cerrado=False), empty_label="--- Id Liquidación ---", label="Identificador de la Liquidación")
    ubicacion = forms.ModelChoiceField(queryset=Ubicacion.objects.filter(activo=True), empty_label="--- Seleccionar ---", label="Ubicación")
    legajo = forms.IntegerField()
    codigo = forms.IntegerField(label="Código del concepto")
    importe = forms.FloatField()
    observaciones = forms.CharField(widget=forms.Textarea, required=False)

# Mixin con Tipos de estado para los formularios
class BuscarMovMesMixin(forms.Form):
    TIPO_ESTADO = [
        ('T', 'Todos'),
        ('P', 'PENDIENTES'),
        ('Y', 'YA PROCESADOS / NO PENDIENTES')
    ]
    estado = forms.ChoiceField(choices=TIPO_ESTADO)

    class Meta:
        abstract = True
class BuscarMovMesLiqForm(BuscarMovMesMixin):
    anio = forms.IntegerField(label='Año')
    periodo = forms.ChoiceField(choices=IdLiquidacion.Meses.choices, label='Mes')
    

class BuscarMovMesBenefForm(BuscarMovMesMixin):
    ubicacion = forms.ModelChoiceField(queryset=Ubicacion.objects.all(), empty_label='--- Seleccionar ---', label='Ubicación / Localidad')
    legajo = forms.IntegerField()

class BuscarMovMesConceptoForm(BuscarMovMesMixin):
    codigo = forms.IntegerField()

