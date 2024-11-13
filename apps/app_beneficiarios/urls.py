from django.urls import path 
from .views import (
    BeneficiarioDetailView,
    BeneficiarioListView,
    BeneficiarioCreateView,
    BeneficiarioUpdateView,
    buscar_beneficiarios,
    generar_reportes_xlsx
)

app_name = 'beneficiarios'

urlpatterns = [
    path('', BeneficiarioListView.as_view(), name='listar' ),
    path('buscar/', buscar_beneficiarios, name='buscar'),
    path('detalle/<int:pk>/', BeneficiarioDetailView.as_view(), name='detalle'),
    path('crear/', BeneficiarioCreateView.as_view(), name='crear'),
    path('actualizar/<int:pk>/', BeneficiarioUpdateView.as_view(), name='update'),
    path('reportes/', generar_reportes_xlsx, name='reportes'),
]
