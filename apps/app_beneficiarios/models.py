from django.db import models
from django.urls import reverse
from apps.app_ubicacion.models import Ubicacion
from apps.app_tipo_pensiones.models import TipoPension

from apps.principal.mixins import RegistroCargaMixin

# Create your models here.
class Beneficiario(RegistroCargaMixin):
    """
    Representa a los beneficiarios de las pensiones a la vejez
    """
    class TipoDocumento(models.TextChoices):
        DNI = '03', 'DNI'
        OTRO = '00', 'OTRO'

    class Genero(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMENINO = 'F', 'Femenino'
        NO_BINARIO = 'X', 'No Binario'
        NO_DECLARADO = 'N', 'No Declarado'


    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.PROTECT)
    legajo = models.PositiveIntegerField()
    apellido_y_nombre = models.CharField(max_length=40)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(choices=Genero.choices, max_length=1, default=Genero.NO_DECLARADO)
    imagen = models.ImageField(upload_to='beneficiarios/img', default='user_generic.png')
    documento_tipo = models.CharField(choices=TipoDocumento.choices, max_length=2, default=TipoDocumento.DNI)
    documento = models.PositiveIntegerField(unique=True)
    cuil = models.PositiveBigIntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=40, default='SIN INFORMACIÓN DISPONIBLE')
    tipo_pension = models.ForeignKey(TipoPension, on_delete=models.PROTECT)
    cobra_sac = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)


    def __str__(self):
        return F"{self.ubicacion} {str(self.legajo).zfill(4) } | {self.apellido_y_nombre.upper() } [{self.documento_tipo}: {self.documento}]"
    
    class Meta:
        constraints  = [models.UniqueConstraint(fields=['ubicacion', 'legajo'], name='legajo_unico')]
        ordering = [ 'ubicacion', 'legajo', 'tipo_pension' ]
        indexes = [
            models.Index(fields=['apellido_y_nombre', ]),
            models.Index(fields=['documento', ]),
            models.Index(fields=['tipo_pension',])]
        index_together = [
            ['ubicacion', 'legajo']
        ]

    def get_absolute_url(self):
        return reverse("beneficiarios:detalle", kwargs={"pk": self.pk})
    