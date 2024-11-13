from django.urls import path
from .views import (generar_detalle_liquidacion,  
                    generar_reporte_csv_liquidacion, 
                    generar_reporte_xlsx_liquidacion, 
                    generar_recibo_pdf, 
                    simulador_recibo)


app_name = 'detalle_liquidacion'

urlpatterns = [
    path('ejecutar/', generar_detalle_liquidacion, name='generar_menu'),
    path('ejecutar/<int:pk>/', generar_detalle_liquidacion, name='generar_liquidacion'),
    path('detalle-xlsx/<int:idliq>/', generar_reporte_xlsx_liquidacion, name='reporte_excel'),
    path('simulador/', simulador_recibo, name='buscar_recibos'),
    path('recibos/<int:idliq>/', generar_recibo_pdf, name='recibos')
]