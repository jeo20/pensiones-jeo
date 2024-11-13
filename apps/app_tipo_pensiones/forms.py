from django import forms 
from .models import TipoPension

opciones = (('', '-- TODOS --'),
            ('T', 'ACTIVOS'),
            ('F', 'INACTIVOS'))

class BuscarPensionesForm(forms.Form):
    codigo_numerico = forms.IntegerField(required=False, label='Código Numérico')
    descripcion_corta = forms.CharField(max_length=4, required=False, label='Descripción Corta')
    descripcion = forms.CharField(max_length=120, widget=forms.Textarea, required=False, label='Descripción')
    estado = forms.ChoiceField(choices=opciones, required=False)
