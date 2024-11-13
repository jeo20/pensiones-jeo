from django.db import models

class RegistroCargaMixin(models.Model):
    """
    Mixin para unificar los tipos de registro de cargas
    """
    class TipoCarga(models.TextChoices):
        USUARIO = 'U', 'Carga Manual'
        MASIVA = 'M', 'Carga Masiva desde Archivo'
        API    = 'A', 'Carga a través de API'

    tipo_carga = models.CharField(max_length=1, choices=TipoCarga.choices, default=TipoCarga.USUARIO)
    creado_usuario = models.CharField(max_length=30, default='---')
    modificado_usuario = models.CharField(max_length=30, default='---')

    class Meta:
        abstract=True
