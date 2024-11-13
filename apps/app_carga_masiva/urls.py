from django.urls import path 

from .views import (
    carga_masiva_view,
    cambiar_estado_view
)

app_name = 'carga_masiva'

urlpatterns = [
    path('', carga_masiva_view, name='carga'),
    path('beneficiarios/', cambiar_estado_view, name='cambiar_estado')
]
