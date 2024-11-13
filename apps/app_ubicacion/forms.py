from django import forms 

from .models import Ubicacion

opciones = (('', '-- TODOS --'),
            ('T', 'ACTIVOS'),
            ('F', 'INACTIVOS'))

class BuscarUbicacionForm(forms.Form):
    nombre = forms.CharField(max_length=40, required=False)
    codigo_postal = forms.CharField(max_length=8, required=False)
    estado = forms.ChoiceField(choices=opciones, required=False)