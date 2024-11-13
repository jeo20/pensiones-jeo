from django.db import models
from apps.app_beneficiarios.models import Beneficiario
from apps.app_codigos.models import Codigo
from apps.app_id_liquidacion.models import IdLiquidacion

from apps.principal.mixins import RegistroCargaMixin

# Create your models here.
class MovimientoMensual(RegistroCargaMixin):
    """
    Novedades / Particularidades a incluir en una liquidación
    """  

    id_liquidacion = models.ForeignKey(IdLiquidacion, on_delete=models.CASCADE)
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.PROTECT)
    codigo = models.ForeignKey(Codigo, on_delete=models.PROTECT)
    importe = models.FloatField()
    pendiente = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modificado', 'id_liquidacion', 'beneficiario']

    def __str__(self):
        return F"{self.id_liquidacion.descripcion} | {self.beneficiario} Código: {self.codigo} Importe: $ {self.importe}"