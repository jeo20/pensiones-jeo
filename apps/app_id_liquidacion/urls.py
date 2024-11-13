from django.urls import path
from .views import (
    IdLiquidacionListView, 
    IdLiquidacionAbiertaListView,
    IdLiquidacionCerradaListView,
    IdLiquidacionCreateView, 
    id_liquidacion_buscar,
    IdLiquidacionUpdateView,
    id_liquidacion_relacionados,
    id_liquidacion_cambio_estado
)

app_name = 'id_liquidacion'

urlpatterns = [
    path('', IdLiquidacionListView.as_view(), name='listar'),
    path('abiertas/', IdLiquidacionAbiertaListView.as_view(), name='listar_abiertas'),
    path('cerradas/', IdLiquidacionCerradaListView.as_view(), name='listar_cerradas'),
    path('crear/', IdLiquidacionCreateView.as_view(), name='crear'),
    path('buscar/', id_liquidacion_buscar, name='buscar' ),
    path('actualizar/<int:pk>/', IdLiquidacionUpdateView.as_view(), name='update'),
    path('detalle/<int:pk>/', id_liquidacion_relacionados, name='id_liquidacion_relacionados'),
    path('cambio-estado/<int:pk>/', id_liquidacion_cambio_estado, name='cambio_estado' )
]
