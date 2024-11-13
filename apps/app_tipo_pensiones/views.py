from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView
from .models import TipoPension
from .forms import BuscarPensionesForm

# Create your views here.
campos = ['codigo_numerico', 'descripcion_corta', 'descripcion', 'activo']


class PensionCreateView(LoginRequiredMixin, CreateView):
    model = TipoPension
    fields = campos
    extra_context = { 'titulo': 'Tipos de Pensiones', 'subtitulo': 'Crear nuevo Tipo de Pensión'}
    template_name = 'crear.html'
    success_url = '/pensiones'

class PensionUpdateView(LoginRequiredMixin, UpdateView):
    model = TipoPension
    fields = campos
    extra_context = { 'titulo': 'Tipos de Pensiones', 'subtitulo': 'Actualizar Tipo de Pensión'}
    template_name = 'crear.html'
    success_url = '/pensiones'
class PensionListView(LoginRequiredMixin, ListView):
    model = TipoPension
    fields = '__all__'
    paginate_by = 12
    extra_context = { 'titulo': 'Tipos de Pensiones', 'subtitulo': 'Listado de Tipo de Pensión', 'template_tabla': 'pensiones/tabla.html'}
    template_name = 'lista.html'


@login_required
def buscar_pension_view(request):
    context = {'titulo': 'Pensiones',
               'subtitulo': 'Búsqueda de Tipos de Pensiones',
               'template_tabla': 'pensiones/tabla.html',
               'form': BuscarPensionesForm(),
               'mensaje': 'Ingrese los criterios de búsqueda',
               'object_list': None}
    
    if request.method == 'POST':
        form = BuscarPensionesForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data 

            kwargs = {}

            if cd['codigo_numerico']:
                kwargs['codigo_numerico'] = cd['codigo_numerico']

            if cd['descripcion_corta']:
                kwargs['descripcion_corta__icontains'] = cd['descripcion_corta']

            if cd['descripcion']:
                kwargs['descripcion__icontains'] = cd['descripcion']

            if cd['estado']:
                kwargs['activo'] = True if cd['estado'] == 'T' else False

            object_list = TipoPension.objects.filter(**kwargs)

            if len(object_list) == 0:
                context['mensaje'] = 'No hay resultados con los criterios de búsqueda solicitados'
            else:
                context['object_list'] = object_list
                context['mensaje'] = None 
    
    return render(request, 'buscar.html', context)