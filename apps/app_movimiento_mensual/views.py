from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    UpdateView
)

from .models import MovimientoMensual
from apps.app_id_liquidacion.models import IdLiquidacion
from apps.app_codigos.models import Codigo
from apps.app_beneficiarios.models import Beneficiario
from .forms import MovMesForm, BuscarMovMesLiqForm, BuscarMovMesBenefForm, BuscarMovMesConceptoForm

# Create your views here.
@login_required
def mov_mes_create_view(request):
    """
    Crea un nuevo objeto de la clase MovimientoMensual, relacionado a
    - Un ID de liquidación
    - Un Usuario
    - Un Concepto / Código
    """
    form = None

    if request.method == 'GET':
        form = MovMesForm()
            
    if request.method == 'POST':
        form = MovMesForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            try:
                beneficiario = Beneficiario.objects.filter(ubicacion=cd['ubicacion'], legajo=cd['legajo']).first()
                if beneficiario is None:
                    raise Exception("No existe el Beneficiario")
                codigo = Codigo.objects.filter(codigo_numerico=cd['codigo'], activo=True, pension=beneficiario.tipo_pension).first()
                if codigo is None:
                    raise Exception("No existe el código")
                MovimientoMensual.objects.create( id_liquidacion = cd['id_liquidacion'],
                                                 beneficiario = beneficiario, 
                                                codigo = codigo,
                                                creado_usuario = request.user.username,
                                                importe = cd['importe'],
                                                observaciones=cd['observaciones'])
            except Exception as e:
                return render(request, 'crear.html', { 'form': form, 'titulo': 'Movimientos Mensuales', 'subtitulo': f'Actualizar Movimientos Mensuales / Ha ocurrido un error: {e}' })
            
            form = MovMesForm()

    return render(request, 'crear.html', { 'form': form, 'titulo': 'Movimientos Mensuales', 'subtitulo': 'Actualizar Movimientos Mensuales' })



class MovMesListView(LoginRequiredMixin, ListView):
    model = MovimientoMensual
    fields = ['id_liquidacion', 'beneficiario', 'codigo', 'modificado' ]
    template_name = 'lista.html'
    extra_context = { 'titulo': 'Movimientos Mensuales', 'subtitulo': 'Listado de Movimientos Mensuales', 'template_tabla': 'movmes/tabla.html'}
    paginate_by = 12


class MovMesUpdateView(LoginRequiredMixin, UpdateView):
    model = MovimientoMensual
    fields = ['id_liquidacion', 'beneficiario', 'codigo', 'importe', 'pendiente', 'observaciones' ]
    template_name = 'crear.html'
    extra_context = {'titulo': 'Movimientos Mensuales', 'subtitulo': 'Actualizar Movimientos Mensuales'}
    success_url = '/movmes/'

    def form_valid(self, form):
        form.instance.modificado_usuario = self.request.user.username
        return super().form_valid(form)


@login_required
def movmes_cambiar_estado(request, pk):
    """
    Pasa a NO PENDIENTE el movimiento mensual que de identifica con el pk
    """
    movmes = get_object_or_404(MovimientoMensual, pk=pk)
    movmes.pendiente = False
    movmes.modificado_usuario = request.user.username
    movmes.save()
    
    return redirect(reverse('movmes:listar'))


@login_required
def buscar_movmes(request, criterio : str = None):
    """
    Función de búsqueda multicriterio
    
    Parameters
    ----------
    criterio : str optional
        Si el valor es L, consulta por movimientos relacionados a una liquidación
        Si el valor es B, consulta por movimientos relacionados a un Beneficiario
        Otro valor, simplemente renderiza el template de búsqueda
    """

    form_movmes_liq = BuscarMovMesLiqForm()
    form_movmes_benef = BuscarMovMesBenefForm()
    form_movmes_concepto = BuscarMovMesConceptoForm()
    object_list = None
    mensaje = 'Ingrese los criterios de búsqueda'
    criterios = ''
    cd = dict()

    if request.method == 'POST':

        if criterio == 'L':
            form = BuscarMovMesLiqForm(request.POST)
            criterios = 'Búsqueda por AÑO/PERÍODO/LIQUIDACIÓN'
            if form.is_valid():
                cd = form.cleaned_data

                object_list = MovimientoMensual.objects.filter(id_liquidacion__anio=cd['anio'], 
                                                               id_liquidacion__mes=cd['periodo'])
                
        elif criterio == 'B':
            form = BuscarMovMesBenefForm(request.POST)
            criterios = 'Búsqueda por BENEFICIARIO'
            if form.is_valid():
                cd = form.cleaned_data

                object_list = MovimientoMensual.objects.filter(beneficiario__ubicacion=cd['ubicacion'], beneficiario__legajo=cd['legajo'])

        elif criterio == 'C':
            form = BuscarMovMesConceptoForm(request.POST)
            criterios = 'Búsqueda por BENEFICIARIO'
            if form.is_valid():
                cd = form.cleaned_data

                object_list = MovimientoMensual.objects.filter(codigo__codigo_numerico=cd['codigo'])

    
        if not object_list:
            mensaje = 'No hay MOVIMIENTOS que coincidan con esos criterios de búsqueda'
        else:
            if cd.get('estado') == 'P':
                object_list = object_list.filter(pendiente=True)
            elif cd.get('estado') == 'Y':
                object_list = object_list.filter(pendiente=False)
        

    return render(request, 'movmes/buscar.html', {'form1': form_movmes_liq,
                                                  'form2': form_movmes_benef,
                                                  'form3': form_movmes_concepto,
                                                  'object_list': object_list,
                                                  'mensaje':mensaje,
                                                  'criterios': criterios})