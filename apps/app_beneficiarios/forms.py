from django import forms

from apps.app_ubicacion.models import Ubicacion
from apps.app_tipo_pensiones.models import TipoPension
from apps.app_beneficiarios.models import Beneficiario

class BusquedaBeneficiario(forms.Form):
    CAMPOS = (('APE', 'APELLIDOS Y NOMBRES'),
              ('DNI', 'NÚMERO DE DOCUMENTO'),
              ('LEG', 'NÚMERO DE LEGAJO'))
    
    campo = forms.ChoiceField(choices=CAMPOS)
    criterio = forms.CharField(max_length=50)
    

vacio = '-- TODOS --'
opciones = [('', vacio)]

estados = (('', '-- TODOS --'),
            ('T', 'ACTIVOS'),
            ('F', 'INACTIVOS'))
class ReporteBeneficiariosForm(forms.Form):
    nombre_reporte = forms.CharField(max_length=20)
    ubicacion = forms.ModelMultipleChoiceField(queryset=Ubicacion.objects.filter(activo=True), 
                                       required=False, 
                                       label='Ubicación')
    tipo_pension = forms.ModelMultipleChoiceField(queryset=TipoPension.objects.all(),  
                                          required=False, 
                                          label='Tipo Pensión')
    genero = forms.ChoiceField(choices=opciones + Beneficiario.Genero.choices,  
                               label='Género',
                               required=False)
    estado = forms.ChoiceField(choices=estados, required=False)
    sac = forms.ChoiceField(choices=estados, 
                            label='Cobra SAC', required=False)