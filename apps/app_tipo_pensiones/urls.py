from django.urls import path
from .views import (PensionCreateView, 
                    PensionListView, 
                    PensionUpdateView,
                    buscar_pension_view)

app_name = 'pensiones'

urlpatterns = [
    path('', PensionListView.as_view(), name='listar'),
    path('crear/', PensionCreateView.as_view(), name='crear'),
    path('modificar/<pk>/', PensionUpdateView.as_view(), name='update'),
    path('buscar/', buscar_pension_view, name='buscar'),
]
