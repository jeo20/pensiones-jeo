from django import forms 


opciones_a_importar = (('B', 'BENEFICIARIOS'),
                       ('M', 'MOVIMIENTOS MENSUALES'),
                       ('C', 'CONCEPTOS'),
                       ('U', 'UBICACIONES / LOCALIDADES'),
                       ('P', 'TIPOS DE PENSIONES'))

# Formulario para subir archivos de carga masiva
class CargaMasivaForm(forms.Form):
    entidad = forms.ChoiceField(choices=opciones_a_importar)
    archivo = forms.FileField()


class CambioEstadoMasivoForm(forms.Form):
    archivo = forms.FileField()