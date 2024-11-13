from django.db import models
from django.utils import timezone

# Create your models here.
class IdLiquidacion(models.Model):
    """
    Identificador de la liquidación, relacionando período y tipo de liquidación
    """

    class Meses(models.TextChoices):
        ENERO = '01ENE', 'ENERO'
        FEBRERO = '02FEB', 'FEBRERO'
        MARZO = '03MRZ', 'MARZO'
        ABRIL = '04ABR', 'ABRIL'
        MAYO = '05MAY', 'MAYO'
        JUNIO = '06JUN', 'JUNIO'
        JULIO = '07JUL', 'JULIO'
        AGOSTO = '08AGO', 'AGOSTO'
        SEPTIEMBRE = '09SEP', 'SEPTIEMBRE'
        OCTUBRE = '10OCT', 'OCTUBRE'
        NOVIEMBRE = '11NOV', 'NOVIEMBRE'
        DICIEMBRE = '12DIC', 'DICIEMBRE'
        SAC1 = '13SC1', 'SAC PRIMERA CUOTA'
        SAC2 = '14SC2', 'SAC SEGUNDA CUOTA'

    anio = models.PositiveIntegerField(verbose_name='año')
    mes = models.CharField(choices=Meses.choices, max_length=5, verbose_name='período')
    descripcion = models.CharField(max_length=40)
    fecha_pago = models.DateField(default=timezone.now)
    cerrado = models.BooleanField(default=False)
    fecha_ultima_ejecucion = models.DateTimeField(null=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    creado_usuario = models.CharField(max_length=30, default='ADMIN')
    modificado_usuario = models.CharField(max_length=30, default='ADMIN')

    class Meta:
        ordering = [ '-anio', '-mes', 'modificado']

    def __str__(self):
        return F"{self.anio} {self.mes} {self.descripcion}"
