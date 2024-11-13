from django.urls import path
from .views import (UbicacionCreateView, 
                    UbicacionListView, 
                    UbicacionUpdateView,
                    buscar_ubicaciones_view
                    )

app_name = 'ubicaciones'

urlpatterns = [
    path('', UbicacionListView.as_view(), name='listar'),
    path('crear/', UbicacionCreateView.as_view(), name='crear'),
    path('buscar/', buscar_ubicaciones_view, name='buscar'),
    path('modificar/<pk>/', UbicacionUpdateView.as_view(), name='update'),
]
