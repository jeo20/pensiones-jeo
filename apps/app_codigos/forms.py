from django import forms 

from apps.app_codigos.models import Codigo
from apps.app_tipo_pensiones.models import TipoPension

seleccione = '-- SELECCIONE --'
opciones = [('', '-- Todos --'),]

class ConceptoBuscarForm(forms.Form):
    codigo_numerico = forms.IntegerField(required=False, label='Código Numérico', initial=None)
    tipo_concepto = forms.ChoiceField(choices=opciones + Codigo.TipoConcepto.choices, required=False, label='Tipo de Concepto')
    tipo_calculo = forms.ChoiceField(choices=opciones + Codigo.TipoCalculo.choices, required=False, label='Modalidad de Cálculo')
    signo = forms.ChoiceField(choices=opciones + Codigo.SignoImporte.choices, required=False, label='Signo')
    tipo_pension = forms.ModelChoiceField(queryset=TipoPension.objects.filter(activo=True), required=False, label='Tipo de Pensión', empty_label=seleccione, initial=None)
