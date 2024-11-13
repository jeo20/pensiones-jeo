from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import render
from .models import Ubicacion
from .forms import BuscarUbicacionForm

# Create your views here.
class UbicacionListView(LoginRequiredMixin, ListView):
    model = Ubicacion
    fields = '__all__'
    extra_context = { 'titulo': 'Ubicaciones', 'subtitulo': 'Listado de Ubicaciones', 'template_tabla': 'ubicacion/tabla.html'}
    template_name = 'lista.html'
    paginate_by = 12


class UbicacionCreateView(LoginRequiredMixin, CreateView):
    model = Ubicacion
    fields = ['localidad', 'nombre', 'codigo_postal', 'activo']
    extra_context = { 'titulo': 'Ubicaciones', 'subtitulo': 'Crear nueva Ubicación'}
    template_name = 'crear.html'
    success_url = '/ubicaciones'

class UbicacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Ubicacion
    fields = ['localidad', 'nombre', 'codigo_postal', 'activo']
    extra_context = { 'titulo': 'Ubicaciones', 'subtitulo': 'Actualizar Ubicación'}
    template_name = 'crear.html'
    success_url = '/ubicaciones'


def buscar_ubicaciones_view(request):
    context = {'titulo': 'Ubicaciones',
               'subtitulo': 'Buscar Ubicaciones / Localidades',
               'mensaje': 'Ingrese los criterios de búsqueda',
               'object_list': None,
               'form': BuscarUbicacionForm(),
               'template_tabla': 'ubicacion/tabla.html'}
    
    kwargs = {}
    
    if request.method == 'POST':
        form = BuscarUbicacionForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            if cd['nombre']:
                kwargs['nombre__icontains'] = cd['nombre']

            if cd['codigo_postal']:
                kwargs['codigo_postal__icontains'] = cd['codigo_postal']

            if cd['estado'] != '':
                kwargs['activo'] = True if cd['estado'] == 'T' else False 

            object_list = Ubicacion.objects.filter(**kwargs)

            if len(object_list) == 0:
                context['mensaje'] = 'No hay resultados con los criterios solicitados'
            else:
                context['object_list'] = object_list

    return render(request, 'buscar.html', context )
            