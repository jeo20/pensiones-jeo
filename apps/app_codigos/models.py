from django.db import models
from apps.app_tipo_pensiones.models import TipoPension

from apps.principal.mixins import RegistroCargaMixin

# Create your models here.
class Codigo(RegistroCargaMixin):
    """
    Representa los códigos/conceptos a liquidar
    Dependen del tipo de pensión
    Están categorizados como pagos o descuentos
    El tipo de cálculo se utiliza en el momento de la liquidación para determinar el valor del campo
    """

    class TipoConcepto(models.TextChoices):
        REMUNERATIVO = 'R', 'Remunerativo'
        NO_REMUNERATIVO = 'N', 'No Remunerativo'
        DESCUENTO = 'D', 'Descuento'
        REDONDEO_POSITIVO = 'X', 'Redondeo Remuneraciones'
        REDONDEO_NEGATIVO = 'Y', 'Redondeo Deducciones'
    

    class TipoCalculo(models.TextChoices):
        PORC_SOBRE_REMUNERATIVO = 'P', 'Porcentaje sobre Remunerativo'
        PORC_SOBRE_TOTAL_PAGO = 'T', 'Porcentaje sobre Total Pago'
        VALOR_FIJO = 'F', 'Valor Fijo'

    class SignoImporte(models.TextChoices):
        POSITIVO = 'P', 'SUMA'
        NEGATIVO = 'N', 'RESTA'

    codigo_numerico = models.PositiveIntegerField(verbose_name='Código Numérico')
    descripcion = models.CharField(max_length=25, verbose_name='Descripción')
    tipo = models.CharField(choices=TipoConcepto.choices, max_length=1, verbose_name='Tipo de Concepto')
    pension = models.ForeignKey(TipoPension, on_delete=models.CASCADE, verbose_name='Aplica al Tipo de Pensión')
    calculo = models.CharField(choices=TipoCalculo.choices, max_length=1, verbose_name='Base de Cálculo')
    signo = models.CharField(choices=SignoImporte.choices, max_length=1, default=SignoImporte.POSITIVO)
    valor = models.FloatField()
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pension', 'codigo_numerico', 'activo', 'modificado']

    def __str__(self):
        return F"[ {self.pension} ] | {self.codigo_numerico}  {self.descripcion}"