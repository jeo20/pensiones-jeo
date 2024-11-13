from django.db import models
from apps.app_id_liquidacion.models import IdLiquidacion
from apps.app_ubicacion.models import Ubicacion

# Create your models here.
class DetalleLiquidacion(models.Model):
    """
    Ítems que componen una liquidación
    Relación beneficiarió / período / conceptos / importes
    """
    
    liquidacion = models.ForeignKey(IdLiquidacion, on_delete=models.CASCADE)
    recibo = models.PositiveIntegerField(default=0)
    localidad = models.ForeignKey(Ubicacion, on_delete=models.RESTRICT)
    legajo = models.PositiveIntegerField()
    beneficiario = models.CharField(max_length=25)
    documento = models.PositiveIntegerField()
    cuil = models.PositiveBigIntegerField(blank=True, null=True)
    tipo_pension = models.PositiveIntegerField()
    codigo = models.PositiveIntegerField()
    codigo_descripcion = models.CharField(max_length=25)
    codigo_tipo = models.CharField(max_length=25)
    importe = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-liquidacion', 'localidad', 'legajo', 'codigo']

    def __str__(self):
        return F"{self.liquidacion};{self.localidad};{self.legajo};{self.beneficiario};{self.tipo_pension};{self.codigo};{self.codigo_descripcion};{self.codigo_tipo};{self.importe} "