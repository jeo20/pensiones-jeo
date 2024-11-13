"""pendat_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('apps.principal.urls', namespace='principal')),
    #Autenticación
    path('login/', auth_views.LoginView.as_view(extra_context={ 'titulo': 'Login', 'subtitulo': 'Iniciar sesión en el Sistema'}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Admin
    path('admin/', admin.site.urls),
    # Aplicaciones
    path('idliquidaciones/', include('apps.app_id_liquidacion.urls', namespace='id_liquidacion')),
    path('liquidaciones/', include('apps.app_detalle_liquidacion.urls', namespace='detalle_liquidacion')),
    path('beneficiarios/', include('apps.app_beneficiarios.urls', namespace='app_beneficiarios')),
    path('movmes/', include('apps.app_movimiento_mensual.urls', namespace='movmes')),
    path('pensiones/', include('apps.app_tipo_pensiones.urls', namespace='pensiones')),
    path('ubicaciones/', include('apps.app_ubicacion.urls', namespace='ubicaciones')),
    path('conceptos/', include('apps.app_codigos.urls', namespace='conceptos')),
    path('carga-masiva/', include('apps.app_carga_masiva.urls', namespace='carga_masiva')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
