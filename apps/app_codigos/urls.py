from django.urls import path
from .views import (ConceptoCreateView, 
                    ConceptoListView, 
                    ConceptoUpdateView, 
                    concepto_cambiar_estado, 
                    ConceptoListViewInactivos,
                    buscar_conceptos)

app_name = 'conceptos'

urlpatterns = [
    path('', ConceptoListView.as_view(), name='listar'),
    path('inactivos/', ConceptoListViewInactivos.as_view(), name='inactivos'),
    path('crear/', ConceptoCreateView.as_view(), name='crear'),
    path('buscar/', buscar_conceptos, name='buscar'),
    path('actualizar/<int:pk>/', ConceptoUpdateView.as_view(), name='actualizar'),
    path('cambiar-estado/<int:pk>/', concepto_cambiar_estado, name='cambiar_estado')
]
