from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import IdLiquidacion
from .forms import BuscarIdLiquidacionForm
from apps.app_detalle_liquidacion.models import DetalleLiquidacion
from apps.app_movimiento_mensual.models import MovimientoMensual

# Create your views here.
class IdLiquidacionListView(LoginRequiredMixin, ListView):
    queryset = IdLiquidacion.objects.all()
    paginate_by = 12
    extra_context = { 'titulo': 'Liquidaciones', 'subtitulo': 'Listado COMPLETO de Liquidaciones', 'template_tabla': 'idliqs/tabla.html'}
    template_name = 'lista.html'  

class IdLiquidacionAbiertaListView(LoginRequiredMixin, ListView):
    queryset = IdLiquidacion.objects.filter(cerrado=False)
    paginate_by = 12
    extra_context = { 'titulo': 'Liquidaciones', 'subtitulo': 'Listado de Liquidaciones ABIERTAS', 'template_tabla': 'idliqs/tabla.html'}
    template_name = 'lista.html' 

class IdLiquidacionCerradaListView(LoginRequiredMixin, ListView):
    queryset = IdLiquidacion.objects.filter(cerrado=True)
    paginate_by = 12
    extra_context = { 'titulo': 'Liquidaciones', 'subtitulo': 'Listado de Liquidaciones CERRADAS', 'template_tabla': 'idliqs/tabla.html'}
    template_name = 'lista.html' 


class IdLiquidacionCreateView(LoginRequiredMixin, CreateView):
    model = IdLiquidacion
    fields = ['anio', 'mes', 'descripcion', 'fecha_pago']
    extra_context = {'titulo': 'ID de Liquidación', 'subtitulo': 'Crear nueva Liquidación'}
    template_name = 'crear.html'
    success_url = '/idliquidaciones'

    def form_valid(self, form):
        form.instance.creado_usuario = self.request.user.username
        return super().form_valid(form)

class IdLiquidacionUpdateView(LoginRequiredMixin, UpdateView):
    model = IdLiquidacion
    fields = ['anio', 'mes', 'descripcion', 'fecha_pago']
    extra_context = {'titulo': 'ID de Liquidación', 'subtitulo': 'Modificar Liquidación'}
    template_name = 'crear.html'
    success_url = '/idliquidaciones'

    def form_valid(self, form):
        form.instance.modificado_usuario = self.request.user.username
        return super().form_valid(form)



def id_liquidacion_relacionados(request, pk):
    """
    Recupera la totalidad de los movimientos relacionados a una liquidación
    Actualmente Vista no mapeada a una URL
    """
    id_liq = get_object_or_404(IdLiquidacion, pk=pk)
    object_list = DetalleLiquidacion.objects.filter(liquidacion=id_liq)

    return render(request, 'idliqs/detalle.html', {
        'object_list': object_list,
    })


@login_required
def id_liquidacion_cambio_estado(request, pk):
    """
    Cierre de la liquidación y de todos los movimientos relacionados
    """
    id_liq = get_object_or_404(IdLiquidacion, pk=pk)
    id_liq.cerrado = True
    id_liq.modificado_usuario = request.user.username
    id_liq.save()
    # Cierro todos los movimientos relacionados
    MovimientoMensual.objects.filter(id_liquidacion=id_liq).update(pendiente=False)

    return redirect(reverse('id_liquidacion:listar_cerradas'))


@login_required
def id_liquidacion_buscar(request):
    """
    Búsqueda multiparamétrica de liquidaciones
    """

    form = BuscarIdLiquidacionForm()
    object_list = None
    mensaje = 'Ingrese los criterios de búsqueda'

    if request.method == 'POST':
        form = BuscarIdLiquidacionForm(request.POST)
        mensaje = ''

        if form.is_valid():
            cd = form.cleaned_data
            cd_anio = cd['anio']
            cd_periodo = cd['periodo']

            if cd_anio is None and cd_periodo != '':
                object_list = IdLiquidacion.objects.filter(mes=cd_periodo)
            
            elif cd_anio is not None and cd_periodo == '':
                object_list = IdLiquidacion.objects.filter(anio=cd_anio)

            elif cd_anio is not None and cd_periodo != '':
                object_list = IdLiquidacion.objects.filter(mes=cd_periodo, anio=cd_anio)
            else:
                object_list = IdLiquidacion.objects.all() 

            if len(object_list) == 0:
                mensaje = 'No hay resultados con los criterios solicitados'
            else:
                mensaje = 'Resultados de la búsqueda'
       
    return render(request, 'buscar.html', { 'form': form, 
                                            'titulo': 'Liquidaciones',
                                            'object_list': object_list,
                                            'subtitulo': 'Buscar Liquidaciones',
                                            'mensaje': mensaje, 
                                            'template_tabla': 'idliqs/tabla.html'})
