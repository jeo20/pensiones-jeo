from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.app_id_liquidacion.models import IdLiquidacion
from apps.app_beneficiarios.models import Beneficiario
from apps.app_codigos.models import Codigo

# Create your views here.
@login_required
def home(request):

    liquidaciones_abiertas = IdLiquidacion.objects.filter(cerrado=False).count()
    beneficiarios_activos = Beneficiario.objects.filter(activo=True).count()
    conceptos_activos = Codigo.objects.filter(activo=True).count()

    return render(request, 'principal/home.html', { 'liquidaciones': liquidaciones_abiertas,
                                                   'beneficiarios': beneficiarios_activos,
                                                   'conceptos': conceptos_activos})