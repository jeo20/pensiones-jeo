from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Codigo
from .forms import ConceptoBuscarForm

# Create your views here.
class ConceptoListView(LoginRequiredMixin, ListView):
    queryset = Codigo.objects.filter(activo=True)
    fields = ['codigo_numerico', 'descripcion', 'tipo', 'pension', 'calculo', 'signo', 'valor', 'activo']
    paginate_by = 12
    extra_context = { 'titulo': 'Conceptos', 'subtitulo': 'Listado de Conceptos', 'template_tabla': 'conceptos/tabla.html'}
    template_name = 'lista.html'

class ConceptoListViewInactivos(LoginRequiredMixin, ListView):
    queryset = Codigo.objects.filter(activo=False)
    fields = ['codigo_numerico', 'descripcion', 'tipo', 'pension', 'calculo', 'signo', 'valor', 'activo']
    paginate_by = 12
    extra_context = { 'titulo': 'Conceptos', 'subtitulo': 'Listado de Conceptos', 'template_tabla': 'conceptos/tabla.html'}
    template_name = 'lista.html'    

class ConceptoCreateView(LoginRequiredMixin, CreateView):
    model = Codigo
    fields = ['codigo_numerico', 'descripcion', 'tipo', 'pension', 'calculo', 'signo', 'valor', 'activo' ]
    extra_context = { 'titulo': 'Conceptos', 'subtitulo': 'Crear Concepto'}
    template_name = 'crear.html'
    success_url = '/conceptos/'

    def form_valid(self, form):
        form.instance.modificado_usuario = self.request.user.username
        return super().form_valid(form)


class ConceptoUpdateView(LoginRequiredMixin, UpdateView):
    model = Codigo 
    fields = ['codigo_numerico', 'descripcion', 'tipo', 'pension', 'calculo', 'signo', 'valor', 'activo' ]
    extra_context = { 'titulo': 'Conceptos', 'subtitulo': 'Actualizar Concepto'}
    template_name = 'crear.html'
    success_url = '/conceptos/'

    def form_valid(self, form):
        form.instance.modificado_usuario = self.request.user.username
        return super().form_valid(form)

@login_required
def concepto_cambiar_estado(request, pk):
    codigo = get_object_or_404(Codigo, pk=pk)
    codigo.activo = not codigo.activo
    codigo.modificado_usuario = request.user.username
    codigo.save()
    return redirect(reverse('conceptos:listar'))


@login_required
def buscar_conceptos(request):
    context = { 'mensaje': 'Ingrese los criterios de búsqueda',
                'template_tabla': 'conceptos/tabla.html',
                'object_list': None,
                'titulo': 'Conceptos',
                'subtitulo': 'Búsqueda de conceptos',
                'form': ConceptoBuscarForm()   
    } 

    if request.method == 'POST':
        form = ConceptoBuscarForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            kwargs = {}

            if cd['codigo_numerico']:
                kwargs['codigo_numerico'] = cd['codigo_numerico']

            if cd['tipo_concepto']:
                kwargs['tipo'] = cd['tipo_concepto']     

            if cd['tipo_calculo']:
                kwargs['calculo'] = cd['tipo_calculo']   

            if cd['signo']:
                kwargs['signo'] = cd['signo']    

            if cd['tipo_pension']:
                kwargs['pension'] = cd['tipo_pension']                                                    

            object_list = Codigo.objects.filter(**kwargs)
            
            context['form'] = form
            
            if len(object_list) == 0:
                context['mensaje'] = 'No hay resultados que coincidan con los criterios seleccionados!'
            else:
                context['object_list'] = object_list

    return render(request, 'buscar.html', context)