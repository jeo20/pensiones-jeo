from datetime import date, datetime
from django.shortcuts import render
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required

from apps.app_beneficiarios.models import Beneficiario
from apps.app_ubicacion.models import Ubicacion
from apps.app_tipo_pensiones.models import TipoPension
from apps.app_id_liquidacion.models import IdLiquidacion
from apps.app_codigos.models import Codigo
from apps.app_movimiento_mensual.models import MovimientoMensual

from .forms import CargaMasivaForm, CambioEstadoMasivoForm


#-- Diccionario para identificar dónde se produce el error
operaciones = {
    'B': 'CMBENEFICIARIOS', # Carga Masiva de Beneficiarios
    'M': 'CMMOVMENSUALES',  # Carga Masiva de Movimientos / Novedades Mensuales
    'C': 'CMCONCEPTOS',     # Carga Masiva de Beneficiarios
    'U': 'CMUBICACIONES',   # Carga Masiva de Ubicaciones
    'P': 'CMPENSIONES'      # Carga Masiva de Tipo Pensiones
}


def auxiliar_mensajes_error(operacion: str, posicion : int, mensaje : str) -> str:
    """
    Función auxiliar para componer los mensajes que se muestran tras procesar el 
    archivo de texto con los datos de origen
    La operación sirve para identificar qué tipo de archivo se está procesando
    La posición indica el registro/línea donde se produce el error
    El mensaje devuelve una indicación del motivo por el cual no es posible procesar el dato
    """
    return F"{operacion} {datetime.now()} | Línea {posicion} -> {mensaje}"



def importacion_masiva_beneficiarios(request, registros):
    """
    Función para la carga masiva de Beneficiarios al sistema
    Utiliza un archivo de texto con los campos determinados por posiciones
    ubicación          [0+6]      (int)
    legajo             [6+8]      (int)
    nombres            [14+40]    (char)
    genero             [54+1]     (char)
    tipo_doc           [55+2]     (char)
    documento          [57+8]     (int)
    cuil               [65+11]    (int)
    direccion          [76+40]    (char)
    tipo_pension       [116+6]    (int)
    cobra_sac          [122+1]    (int)
    activo             [123+1]    (int)
    fecha_nacimiento   [124+8]    (int) YYYYMMDD
    """
    REGISTRO_LEN = 133
    errores = []
    operacion = operaciones.get('B')

    for idx, registro in enumerate(registros):
        try:
            registro = registro.decode()

            if len(registro) < REGISTRO_LEN:
                raise Exception('Longitud incorrecta del registro!')
            
            ubicacion  = int(registro[0:6])
            legajo = int(registro[6:6+8])
            nombres = registro[14:14+40].strip()
            genero = registro[54:54+1]
            tipo_doc = registro[55:55+2]
            documento = int(registro[57:57+8])
            cuil = int(registro[65:65+11])
            direccion = registro[76:76+40].strip()
            tipo_pension = int(registro[116:116+6])
            cobra_sac = int(registro[122:122+1])
            activo = int(registro[123:123+1])
            fecha_nacimiento = registro[124:124+8]

            if cobra_sac not in [0, 1]:
                raise Exception('Valor incorrecto para campo COBRA_SAC')
            
            if activo not in [0, 1]:
                raise Exception('Valor incorrecto para campo ACTIVO')

            cobra_sac =  False if (cobra_sac == 0) else True 
            activo =  False if (activo == 0) else True 
        
            ubicacion = Ubicacion.objects.filter(localidad=ubicacion).first()
            tipo_pension = TipoPension.objects.filter(codigo_numerico=tipo_pension).first()

            nuevo_beneficiario = Beneficiario.objects.create(ubicacion=ubicacion,
                                                    legajo=legajo,
                                                    apellido_y_nombre=nombres,
                                                    genero=genero,
                                                    documento_tipo=tipo_doc,
                                                    documento=documento,
                                                    cuil=cuil,
                                                    direccion=direccion,
                                                    tipo_pension=tipo_pension,
                                                    cobra_sac=cobra_sac,
                                                    activo=activo,
                                                    fecha_nacimiento=date(int(fecha_nacimiento[0:4]), int(fecha_nacimiento[4:6]), int(fecha_nacimiento[6:])),
                                                    creado_usuario=request.user.username,
                                                    tipo_carga=Beneficiario.TipoCarga.MASIVA)
            nuevo_beneficiario.save()

        except IntegrityError:
            errores.append(auxiliar_mensajes_error(operacion,
                                                            idx+1, 
                                                            'Verifique los valores UBICACIÓN, TIPO DNI, TIPO PENSION, etc'))
            continue 
        except ValueError as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                            idx+1, 
                                                            F'Verifique que no tenga letras u otros caracteres en los campos NUMÉRICOS -> {e}'))
            continue
        except Exception as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                            idx+1, 
                                                            e))
            continue

    return errores


def importacion_masiva_movmes(request, registros):
    """
    Carga masiva de novedades mensuales para liquidar, a partir de un
    archivo de texto en formato campos limitados por posiciones fijas
    
    liquidacion          [0: 6]     (int) <- identificador de la liquidación relacionada
    benef_ubicacion      [6: 6+6]   (int) <- código numérico de la localidad
    benef_legajo         [12: 12+8] (int) <- número de legajo del beneficiario
    concepto             [20: 20+6] (int) <- código numérico que identifica al concepto
    importe_entero       [26: 26+14](int) <- parte entera del importe
    importe_decimal      [40: 40+2] (int) <- parte decimal del importe
    pendiente            [42: 42+1] (int) <- 1 (uno) para que se pague / 0 (cero) para que no se pague
    observaciones        [43: 43+128] (char) <- Observaciones (optativas) sobre el movimiento
    """
    REGISTRO_LEN = 171
    errores = []
    operacion = operaciones.get('M')

    for idx, registro in enumerate(registros):
        try:
            registro = registro.decode() 

            if len(registro) < REGISTRO_LEN:
                raise Exception(F'Longitud incorrecta del registro!')
 
            liquidacion     = int(registro[0: 6])
            benef_ubicacion = int(registro[6: 6+6])
            benef_legajo    = int(registro[12: 12+8])
            concepto        = int(registro[20: 20+6])
            importe_entero  = int(registro[26: 26+14])
            importe_decimal = int(registro[40: 40+2])
            pendiente       = int(registro[42: 42+1])
            observaciones   = registro[43:43+128].strip()   

            # Instancio los objetos que se necesitan para luego crear el movmes
            liquidacion = IdLiquidacion.objects.filter(pk=liquidacion, cerrado=False).first()
            benef_ubicacion = Ubicacion.objects.filter(localidad=benef_ubicacion, activo=True).first()
            beneficiario = Beneficiario.objects.filter(ubicacion=benef_ubicacion, legajo=benef_legajo).first()
            concepto = Codigo.objects.filter(codigo_numerico=concepto, pension=beneficiario.tipo_pension, activo=True).order_by('-modificado').first()
            importe = importe_entero + (importe_decimal / 100) 

            if pendiente not in [0, 1]:
                raise Exception("Valor incorrecto para el campo PENDIENTE")

            pendiente = True if pendiente == 1 else False 
            movmes = MovimientoMensual.objects.create(id_liquidacion=liquidacion,
                                                      beneficiario=beneficiario,
                                                      codigo=concepto,
                                                      importe=importe,
                                                      pendiente=pendiente,
                                                      creado_usuario=request.user.username,
                                                      observaciones=observaciones,
                                                      tipo_carga=MovimientoMensual.TipoCarga.MASIVA)

            movmes.save()
        except IntegrityError:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    'Verifique los valores UBICACIÓN, TIPO DNI, TIPO PENSION, etc'))
            continue 
        except ValueError:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    'Verifique que no tenga letras u otros caracteres en los campos NUMÉRICOS'))
            continue
        except AttributeError as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    'Verificar que el BENEFICIARIO existe y/o que existan CONCEPTOS relacionados a su TIPO DE PENSIÓN'))
            continue
        except Exception as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                   idx+1, 
                                                   e))
            continue

    return errores


def importacion_masiva_conceptos(request, registros):
    """
    Carga masiva de novedades mensuales para liquidar, a partir de un
    archivo de texto en formato campos limitados por posiciones fijas
    codigo_numerico    [0:0+6]   (int)    Código numérico que identifica al concepto
    descripcion        [6:6+25]  (char)   Descripción human-readable del código
    tipo_concepto      [31:31+1] (char)   Definidos en Codigo.TipoConcepto.choices 
    pension            [32:32+8] (int)    Código numérico del tipo de pensión al que aplica
    tipo_calculo       [40:40+1] (char)   Definidos en Codigo.TipoCalculo.choices 
    signo_calculo      [41:41+1] (char)   Definidos en Codigo.SignoImporte.choices 
    importe_entero     [42:42+14] (int)   Parte entera del importe
    importe_decimal    [56:56+2]  (int)   Parte decimal del importe
    activo             [58:58+1]  (int)   1 para activo / 0 para inactivo
    """
    REGISTRO_LEN = 60
    errores = []
    operacion = operaciones.get('C')

    for idx, registro in enumerate(registros):
        try:
            registro = registro.decode() 

            if len(registro) < REGISTRO_LEN:
                raise Exception(F'Longitud incorrecta del registro!')
 
            codigo_numerico = int(registro[0:0+6])
            descripcion     = registro[6:6+25].strip()
            tipo_concepto   = registro[31:31+1]
            pension         = int(registro[32:32+8])
            tipo_calculo    = registro[40:40+1]
            signo_calculo   = registro[41:41+1]
            importe_entero  = int(registro[42:42+14])
            importe_decimal = int(registro[56:56+2])
            activo          = int(registro[58:58+1])

            pension = TipoPension.objects.filter(codigo_numerico=pension, activo=True).first()
            importe = importe_entero + (importe_decimal / 100)

            if activo not in [0, 1]:
                raise Exception('Valor incorrecto para el campo ACTIVO')
            
            if tipo_concepto not in Codigo.TipoConcepto.values:
                raise Exception("Revisar el TIPO DE CONCEPTO cargado")
            
            if tipo_calculo not in Codigo.TipoCalculo.values:
                raise Exception("Revisar el TIPO DE CALCULO cargado")
            
            if signo_calculo not in Codigo.SignoImporte.values:
                raise Exception("Revisar el SIGNO DE CÁLCULO cargado")
            
            activo = True if activo == 1 else False 

            concepto = Codigo.objects.create(codigo_numerico=codigo_numerico,
                                             descripcion=descripcion,
                                             tipo=tipo_concepto,
                                             pension=pension,
                                             calculo=tipo_calculo,
                                             signo=signo_calculo,
                                             valor=importe,
                                             activo=activo,
                                             creado_usuario=request.user.username,
                                             tipo_carga=Codigo.TipoCarga.MASIVA)
            
            concepto.save()

        except IntegrityError as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    'Verifique los valores CÓDIGO NUMÉRICO, TIPOS y PENSIÓN'))
            continue 
        except ValueError as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    'Verifique que no tenga letras u otros caracteres en los campos NUMÉRICOS'))
            continue
        except AttributeError:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    'Verificar que el TIPO DE PENSIÓN existe y que esté ACTIVA'))
            continue
        except Exception as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    e))
            continue

    return errores


def importacion_masiva_ubicacion(request, registros):
    """
    Función para la carga masiva de Ubicaciones / Localidades
    localidad      [0:0+6]   (int)   Código numérico que identifica a la localidad
    nombre         [6: 40+6] (char)  Nombre de la localidad
    codigo_postal  [46:46+8] (char)  Código Postal, soporta la forma Z9400BAJ
    activo         [54:54+1] (int)   1 para activo / 0 para inactivo
    """
    REGISTRO_LEN = 55
    errores = []
    operacion = operaciones.get('U')

    for idx, registro in enumerate(registros):
        try:
            registro = registro.decode() 

            if len(registro) < REGISTRO_LEN:
                raise Exception(F'Longitud incorrecta del registro!')

            localidad     = int(registro[0:0+6]  )
            nombre        = registro[6: 40+6].strip()
            codigo_postal = registro[46:46+8].strip()
            activo        = int(registro[54:54+1])


            if activo not in [0, 1]:
                raise Exception('Valor incorrecto para el campo ACTIVO')           
            activo = True if activo == 1 else False 

            ubicacion = Ubicacion.objects.create(localidad=localidad,
                                                 nombre=nombre,
                                                 codigo_postal=codigo_postal,
                                                 activo=activo,
                                                 creado_usuario=request.user.username,
                                                 tipo_carga=Ubicacion.TipoCarga.MASIVA)
            
            ubicacion.save()

        except IntegrityError as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    'Verifique que el CÓDIGO NUMÉRICO no haya sido asignado antes'))
            continue
        except ValueError as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    'Verifique que no tenga letras u otros caracteres en los campos NUMÉRICOS'))
            continue

        except Exception as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    e))
            continue

    return errores


def importacion_masiva_pensiones(request, registros):
    """
    Función para carga masiva de Tipos de Pensiones
    codigo_numerico      [0:6] (int)        Código numérico ÚNICO que identifica a la pensión
    descripcion_corta    [6:6+4] (char)     Descripción corta para usar en informes/reportes, etc
    descripcion          [10:10+128] (char) Descripción completa del tipo de pensión
    activo               [138:138+1] (int)  1 para activo / 0 para inactivo
    """
    REGISTRO_LEN = 139
    errores = []
    operacion = operaciones.get('P')

    for idx, registro in enumerate(registros):
        try:
            registro = registro.decode() 

            if len(registro) < REGISTRO_LEN:
                raise Exception(F'Longitud incorrecta del registro!')

            codigo_numerico     = int(registro[0:6])
            descripcion_corta   = registro[6:6+4] 
            descripcion         = registro[10:10+128].strip()
            activo              = int(registro[138:138+1])


            if activo not in [0, 1]:
                raise Exception('Valor incorrecto para el campo ACTIVO')           
            activo = True if activo == 1 else False 

            tipo_pension = TipoPension.objects.create(codigo_numerico=codigo_numerico,
                                                      descripcion_corta=descripcion_corta,
                                                      descripcion=descripcion,
                                                      activo=activo,
                                                      creado_usuario= request.user.username,
                                                      tipo_carga=TipoPension.TipoCarga.MASIVA)
            
            tipo_pension.save()

        except IntegrityError as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    'Verifique que el CÓDIGO NUMÉRICO no haya sido asignado antes'))
            continue
        except ValueError as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    'Verifique que no tenga letras u otros caracteres en los campos NUMÉRICOS'))
            continue
        except Exception as e:
            errores.append(auxiliar_mensajes_error(operacion,
                                                    idx+1, 
                                                    e))
            continue

    return errores



# Create your views here.
@login_required
def carga_masiva_view(request):

    form = CargaMasivaForm()
    context = {'titulo': 'Carga Masiva',
               'subtitulo': 'Carga Masiva desde Archivos',
               'errores': []}

    if request.method == 'POST':
        form = CargaMasivaForm(request.POST, request.FILES)

        if form.is_valid():
            context['errores'].append(F"Archivo procesado: {request.FILES['archivo'].name}")
            cd = form.cleaned_data

            registros = request.FILES['archivo'].readlines()

            #-- De acuerdo a la opción elegida en el formulario,
            # llamo a la función adecuada para procesar el archivo
            if cd['entidad'] == 'B':
                context['errores'].extend(importacion_masiva_beneficiarios(request, registros))
            if cd['entidad'] == 'M':
                context['errores'].extend(importacion_masiva_movmes(request, registros))
            if cd['entidad'] == 'C':
                context['errores'].extend(importacion_masiva_conceptos(request, registros))
            if cd['entidad'] == 'U':
                context['errores'].extend(importacion_masiva_ubicacion(request, registros))
            if cd['entidad'] == 'P':
                context['errores'].extend(importacion_masiva_pensiones(request, registros))


    context['form'] = form
    return render(request, 'carga_masiva/subir_archivos.html', context)


@login_required
def cambiar_estado_view(request):
    """
    Cambia el estado ACTIVO a los Beneficiarios
    IMPORTANTE: NO GENERA ALTAS
    Estructura del archivo
    ubicacion         int (6)  -> Código numérico de la ubicación / localidad
    legajo            int (8)  -> Número de legajo del agente
    tipo_documento    char (2) -> Tipo de documento 3 DNI / 0 OTRO
    documento         int (8)  -> Número de documento del beneficiario
    estado            int (1)  -> 1 ACTIVO / 0 INACTIVO
    """
    context = {'titulo': 'Carga Masiva',
               'subtitulo': 'BENEFICIARIOS | Cambio Estado [Masivo]',
               'errores': [],
               'form': CambioEstadoMasivoForm()}

    if request.method == 'POST':
        form = CambioEstadoMasivoForm(request.POST, request.FILES)

        if form.is_valid():
            context['errores'].append(F"Archivo -> {request.FILES['archivo'].name} procesado.")
            registros =  request.FILES['archivo'].readlines()
            for idx, registro in enumerate(registros):
                try:
                    registro = registro.decode()

                    if len(registro) < 25:
                        raise Exception(F'Longitud de registro incorrecta {len(registro)}')

                    ubicacion = int(registro[0:6])
                    legajo    = int(registro[6:14])
                    #tipo_documento = registro[14:16].strip()
                    documento = int(registro[16:24])
                    activo    = int(registro[24:25])

                    if not activo in [0, 1]:
                        raise Exception(F'Línea {idx} Opción inválida para el estado')

                    b = Beneficiario.objects.filter(ubicacion__localidad=ubicacion,
                                                legajo=legajo,
                                                documento=documento)
                    
                    if len(b) == 0:
                        raise Exception('No se pudo localizar el BENEFICIARIO')
                    
                    b.update(activo=activo)
                    
                    context['errores'].append(F"Línea {idx+1}  Beneficiario [ {ubicacion} - {legajo} ] -> Actualizado a estado {activo}")

                except Exception as e:
                    context['errores'].append(F"Línea {idx+1}-> Error: {e}")
                    continue 

    return render(request, 'carga_masiva/subir_archivos.html', context)

