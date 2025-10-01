from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Participante, Pais, Departamento, Provincia, Distrito,
    Profesion, GradoInstruccion, CentroEstudio, TipoCentroEstudio,
    Origen, TipoDocumento
)
from .forms import ParticipanteForm
from Cursos.models import Fact_Curso, Fact_Inscripcion, Dim_Modalidad
import json
from datetime import date


# ===============================
# VISTA CLÁSICA CON FORMULARIO HTML
# ===============================
def buscar_participante(request):
    participante = None
    mensaje_info = None
    dni = request.GET.get('dni')
    tipo_doc_id = request.GET.get('tipo_documento')

    # variables para mantener selección en caso de POST fallido
    selected_pais = selected_departamento = selected_provincia = selected_distrito = None

    if request.method == 'POST':
        dni_post = request.POST.get('dni')
        tipo_doc_post = request.POST.get('tipo_documento')

        participante_existente = Participante.objects.filter(
            dni=dni_post,
            tipo_documento_id=tipo_doc_post
        ).first()

        if participante_existente:
            form = ParticipanteForm(request.POST, instance=participante_existente)
        else:
            form = ParticipanteForm(request.POST)

        selected_pais = request.POST.get('pais')
        selected_departamento = request.POST.get('departamento')
        selected_provincia = request.POST.get('provincia')
        selected_distrito = request.POST.get('distrito')

        form.fields['pais'].queryset = Pais.objects.all()
        form.fields['departamento'].queryset = Departamento.objects.filter(pais_id=selected_pais) if selected_pais else Departamento.objects.none()
        form.fields['provincia'].queryset = Provincia.objects.filter(departamento_id=selected_departamento) if selected_departamento else Provincia.objects.none()
        form.fields['distrito'].queryset = Distrito.objects.filter(provincia_id=selected_provincia) if selected_provincia else Distrito.objects.none()

        if form.is_valid():
            participante = form.save()
            return redirect('participante:seleccionar_curso', id_participante=participante.id)
        else:
            print("DEBUG - request.POST:", dict(request.POST))
            print("DEBUG - form.errors:", form.errors)

    else:
        # GET: búsqueda por dni+tipo_doc
        if dni and tipo_doc_id:
            participante = Participante.objects.filter(
                dni=dni,
                tipo_documento_id=tipo_doc_id
            ).first()

            if participante:
                # participante encontrado: vaciar campos de búsqueda
                dni = ""
                tipo_doc_id = ""
                form = ParticipanteForm(instance=participante)
            else:
                # participante no encontrado: vaciar campos búsqueda y llenar registro con lo ingresado
                dni_temp = dni
                tipo_doc_temp = tipo_doc_id
                dni = ""
                tipo_doc_id = ""
                form = ParticipanteForm(initial={
                    'dni': dni_temp,
                    'tipo_documento': tipo_doc_temp
                })
                mensaje_info = "No existe participante, se registrará."

        else:
            form = ParticipanteForm()

    # Preparar listas para selects
    pais_context_id = selected_pais or (participante.pais.id if participante and participante.pais else None)
    departamento_context_id = selected_departamento or (participante.departamento.id if participante and participante.departamento else None)
    provincia_context_id = selected_provincia or (participante.provincia.id if participante and participante.provincia else None)

    departamentos = Departamento.objects.filter(pais_id=pais_context_id) if pais_context_id else []
    provincias = Provincia.objects.filter(departamento_id=departamento_context_id) if departamento_context_id else []
    distritos = Distrito.objects.filter(provincia_id=provincia_context_id) if provincia_context_id else []

    context = {
        "form": form,
        "participante": participante,
        "mensaje_info": mensaje_info,
        "dni": dni,
        "tipo_doc_id": tipo_doc_id,
        "paises": Pais.objects.all(),
        "departamentos": departamentos,
        "provincias": provincias,
        "distritos": distritos,
        "tipos_documento": TipoDocumento.objects.all(),
        "profesiones": Profesion.objects.all(),
        "grados_instruccion": GradoInstruccion.objects.all(),
        "centros_estudio": CentroEstudio.objects.all(),
        "tipos_centro_estudio": TipoCentroEstudio.objects.all(),
        "origenes": Origen.objects.all(),
        "horas_contacto": [str(h) for h in range(7, 24)],
        "selected_pais": selected_pais,
        "selected_departamento": selected_departamento,
        "selected_provincia": selected_provincia,
        "selected_distrito": selected_distrito,
    }

    return render(request, 'Participante/buscar.html', context)


# ===============================
# VISTA PARA SELECCIONAR CURSO Y REGISTRAR INSCRIPCIÓN
# ===============================
def seleccionar_curso(request, id_participante):
    participante = Participante.objects.get(id=id_participante)
    cursos = Fact_Curso.objects.filter(SitioWebCurso=1)
    modalidades = Dim_Modalidad.objects.filter(IdModalidad__in=[1, 2])

    mostrar_certificado = False
    mensaje_error = None  # Para mostrar errores de validación

    if request.method == 'POST':
        id_curso = request.POST.get('curso')
        id_modalidad_seleccionada = request.POST.get('modalidad')
        desea_certificado = request.POST.get('desea_certificado')

        # VALIDACIONES
        errores = []
        curso_obj = None
        if not id_curso:
            errores.append("Debe seleccionar un curso.")
        else:
            curso_obj = Fact_Curso.objects.get(IdCurso=id_curso)
            if curso_obj.IdModalidad == 3 and not id_modalidad_seleccionada:
                errores.append("Debe seleccionar una modalidad.")
            if curso_obj.IdFormato in [6, 7] and not desea_certificado:
                errores.append("Debe seleccionar su preferencia en el desplegable correspondiente.")
            if curso_obj.IdFormato in [6, 7]:
                mostrar_certificado = True

        if errores:
            mensaje_error = " ".join(errores)
        else:
            # ===========================
            # NUEVO: VERIFICAR INSCRIPCIÓN EXISTENTE
            # ===========================
            id_formateado = f"JAE{str(participante.id).zfill(7)}"
            inscripcion_existente = Fact_Inscripcion.objects.filter(
                IdParticipante=id_formateado,
                IdCurso=curso_obj.IdCurso
            ).first()

            if inscripcion_existente:
                # Si ya existe inscripción, mostrar página especial
                return render(request, 'Participante/inscripcion_existente.html', {
                    "participante": participante,
                    "curso": curso_obj,
                    "inscripcion": inscripcion_existente
                })
            else:
                # CREAR INSCRIPCIÓN NUEVA
                Fact_Inscripcion.objects.create(
                    IdParticipante=id_formateado,
                    IdCurso=curso_obj.IdCurso,
                    IdEstadoEntregaAcreditacion=2,
                    IdEstadoInscripcion=1,
                    UsuarioRegistroInscripcion="Sitio Web",
                    FechaInscripcion=date.today(),
                    IdModalidad=int(id_modalidad_seleccionada) if id_modalidad_seleccionada else None,
                    DeseaCertificadoInscripcion=desea_certificado == '1'
                )
                return render(request, 'Participante/inscripcion_exitosa.html', {
                    "participante": participante,
                    "curso": curso_obj
                })

    context = {
        "participante": participante,
        "cursos": cursos,
        "modalidades": modalidades,
        "mostrar_certificado": mostrar_certificado,
        "mensaje_error": mensaje_error
    }
    return render(request, 'Participante/seleccionar_curso.html', context)


# ===============================
# API JSON: BUSCAR PARTICIPANTE
# ===============================
def buscar_participante_json(request):
    dni = request.GET.get("dni")
    try:
        participante = Participante.objects.get(dni=dni)
        data = {
            "id": participante.id,
            "dni": participante.dni,
            "nombres": participante.nombres,
            "apellido_paterno": participante.apellido_paterno,
            "apellido_materno": participante.apellido_materno,
            "email_principal": participante.email_principal,
            "celular": participante.celular,
            "pais": participante.pais.id if participante.pais else None,
            "departamento": participante.departamento.id if participante.departamento else None,
            "provincia": participante.provincia.id if participante.provincia else None,
            "distrito": participante.distrito.id if participante.distrito else None,
            "tipo_documento": participante.tipo_documento.id if participante.tipo_documento else None,
            "profesion": participante.profesion.id if participante.profesion else None,
            "grado_instruccion": participante.grado_instruccion.id if participante.grado_instruccion else None,
            "centro_estudio": participante.centro_estudio.id if participante.centro_estudio else None,
            "tipo_centro_estudio": participante.tipo_centro_estudio.id if participante.tipo_centro_estudio else None,
            "origen": participante.origen.id if participante.origen else None,
        }
        return JsonResponse({"success": True, "participante": data})
    except Participante.DoesNotExist:
        return JsonResponse({"success": False, "error": "No encontrado"})


# ===============================
# API JSON: REGISTRAR/ACTUALIZAR PARTICIPANTE
# ===============================
@csrf_exempt
def registrar_participante_json(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            dni = data.get("dni")
            participante, created = Participante.objects.update_or_create(
                dni=dni,
                defaults={
                    "nombres": data.get("nombres"),
                    "apellido_paterno": data.get("apellido_paterno"),
                    "apellido_materno": data.get("apellido_materno"),
                    "email_principal": data.get("email_principal"),
                    "celular": data.get("celular"),
                    "pais": Pais.objects.get(id=data.get("pais")) if data.get("pais") else None,
                    "departamento": Departamento.objects.get(id=data.get("departamento")) if data.get(
                        "departamento") else None,
                    "provincia": Provincia.objects.get(id=data.get("provincia")) if data.get("provincia") else None,
                    "distrito": Distrito.objects.get(id=data.get("distrito")) if data.get("distrito") else None,
                    "tipo_documento": TipoDocumento.objects.get(id=data.get("tipo_documento")) if data.get(
                        "tipo_documento") else None,
                    "profesion": Profesion.objects.get(id=data.get("profesion")) if data.get("profesion") else None,
                    "grado_instruccion": GradoInstruccion.objects.get(id=data.get("grado_instruccion")) if data.get(
                        "grado_instruccion") else None,
                    "centro_estudio": CentroEstudio.objects.get(id=data.get("centro_estudio")) if data.get(
                        "centro_estudio") else None,
                    "tipo_centro_estudio": TipoCentroEstudio.objects.get(
                        id=data.get("tipo_centro_estudio")) if data.get("tipo_centro_estudio") else None,
                    "origen": Origen.objects.get(id=data.get("origen")) if data.get("origen") else None,
                }
            )
            return JsonResponse({"success": True, "id": participante.id, "created": created})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Método no permitido"})


# ===============================
# API JSON PARA LISTAR DIMENSIONES (cascada)
# ===============================
def lista_paises(request):
    paises = list(Pais.objects.values('id', 'nombre'))
    return JsonResponse({"success": True, "paises": paises})


def lista_departamentos(request):
    pais_id = request.GET.get('pais_id')
    departamentos = list(Departamento.objects.filter(pais_id=pais_id).values('id', 'nombre')) if pais_id else []
    return JsonResponse({"success": True, "departamentos": departamentos})


def lista_provincias(request):
    departamento_id = request.GET.get('departamento_id')
    provincias = list(
        Provincia.objects.filter(departamento_id=departamento_id).values('id', 'nombre')) if departamento_id else []
    return JsonResponse({"success": True, "provincias": provincias})


def lista_distritos(request):
    provincia_id = request.GET.get('provincia_id')
    distritos = list(Distrito.objects.filter(provincia_id=provincia_id).values('id', 'nombre')) if provincia_id else []
    return JsonResponse({"success": True, "distritos": distritos})
