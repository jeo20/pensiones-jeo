from django.db import models

from apps.principal.mixins import RegistroCargaMixin

# Create your models here.
class Ubicacion(RegistroCargaMixin):
    """
    Ubicación geográfica/de servicio del beneficiario a la pensión
    """
    localidad = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=40)
    codigo_postal = models.CharField(max_length=8, default='9400', blank=True, verbose_name='Código Postal')
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return F"{self.nombre}"
    
    class Meta:
        constraints  = [models.UniqueConstraint(fields=['localidad',], name='localidad')]
        ordering = [ 'localidad', 'nombre', 'codigo_postal' ]
        indexes = [
            models.Index(fields=['localidad', ]),
            models.Index(fields=['nombre', ]),]


