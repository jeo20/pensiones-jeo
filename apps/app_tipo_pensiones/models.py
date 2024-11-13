from django.db import models

from apps.principal.mixins import RegistroCargaMixin

# Create your models here.
class TipoPension(RegistroCargaMixin):
    """
    Información sobre el beneficio a recibir
    """
    codigo_numerico = models.PositiveIntegerField(unique=True, verbose_name='Código Numérico')
    descripcion_corta = models.CharField(max_length=4, verbose_name='Descripción corta (4 car.)')
    descripcion = models.TextField(verbose_name='Descripción detallada')
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return str(self.descripcion_corta)
    
    class Meta:
        ordering = ['codigo_numerico', 'descripcion_corta']

