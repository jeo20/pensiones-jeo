from django.urls import path 
from .views import (
    MovMesListView,
    MovMesUpdateView,
    movmes_cambiar_estado,
    mov_mes_create_view,
    buscar_movmes
)

app_name = 'movmes'

urlpatterns = [
    path('', MovMesListView.as_view(), name='listar'),
    path('crear/', mov_mes_create_view, name='crear'),
    path('actualizar/<int:pk>/', MovMesUpdateView.as_view(), name='update'),
    path('cambiar-estado/<int:pk>/', movmes_cambiar_estado, name='cambiar_estado'),
    path('buscar/', buscar_movmes, name='buscar'),
    path('buscar/<slug:criterio>/', buscar_movmes, name='buscar_criterio')
]

