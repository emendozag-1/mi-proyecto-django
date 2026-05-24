from django.shortcuts import render, redirect, get_object_or_slice
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import date
from Cursos.models import Fact_Curso
from .models import (
    DimTipoCuestionario, FactCuestionario, FactPregunta, 
    FactRespuestaCuestionario
)

# ==========================================================
# 1. SELECCIONAR ENCUESTA
# ==========================================================
def seleccionar_encuesta(request):
    tipos_cuestionario = DimTipoCuestionario.objects.all()
    cursos = Fact_Curso.objects.filter(SitioWebCurso=1)
    
    if request.method == 'POST':
        id_cuestionario = request.POST.get('cuestionario')
        id_curso = request.POST.get('curso')
        
        if id_cuestionario and id_curso:
            return redirect('encuestas:responder_encuesta', id_cuestionario=id_cuestionario, id_curso=id_curso)
            
    context = {
        'tipos_cuestionario': tipos_cuestionario,
        'cursos': cursos,
    }
    return render(request, 'Encuestas/seleccionar_encuesta.html', context)


# ==========================================================
# 2. FORMULARIO DE ENCUESTA (PREGUNTAS DINÁMICAS)
# ==========================================================
def responder_encuesta(request, id_cuestionario, id_curso):
    cuestionario = get_object_or_404(FactCuestionario, IdCuestionario=id_cuestionario)
    curso = get_object_or_404(Fact_Curso, IdCurso=id_curso)
    
    # Se obtienen todas las preguntas. Como se mencionó que Fact_Cuestionario
    # solo enlaza en Fact_RespuestaCuestionario, cargaremos todas las preguntas de FactPregunta
    # o según tu lógica de filtrado de preguntas. Traemos todas para que renderice según TipoPregunta.
    preguntas = FactPregunta.objects.select_related('tipo_pregunta', 'sub_pregunta').all()
    
    # También podemos agruparlas para renderizado o pasarlas ordenadas
    
    if request.method == 'POST':
        errores = []
        respuestas_a_guardar = []
        
        # Validar y procesar respuestas para cada pregunta
        for pregunta in preguntas:
            key = f"pregunta_{pregunta.IdPregunta}"
            valor_respuesta = request.POST.get(key)
            
            # En Django, puedes validar que sea obligatorio
            if not valor_respuesta:
                # Opcional: Validar si quieres hacer obligatorias todas o algunas
                # Si deseas hacer obligatorias todas las preguntas:
                # errores.append(f"Debe responder la pregunta: {pregunta.NombrePregunta}")
                pass
            
            if valor_respuesta:
                respuestas_a_guardar.append(
                    FactRespuestaCuestionario(
                        pregunta=pregunta,
                        cuestionario=cuestionario,
                        IdParticipante=None, # Anónimo
                        curso=curso,
                        IdModulo=None,       # NULL por ahora
                        FechaRespuesta=date.today(),
                        Respuesta=str(valor_respuesta)[:120] # Truncar a 120 caracteres según VARCHAR(120)
                    )
                )
                
        if not errores:
            # Guardado masivo
            for resp in respuestas_a_guardar:
                resp.save()
            return redirect('encuestas:encuesta_exitosa')
        
    context = {
        'cuestionario': cuestionario,
        'curso': curso,
        'preguntas': preguntas,
    }
    return render(request, 'Encuestas/responder_encuesta.html', context)


# ==========================================================
# 3. CONFIRMACIÓN DE ENVÍO
# ==========================================================
def encuesta_exitosa(request):
    return render(request, 'Encuestas/encuesta_exitosa.html')


# ==========================================================
# 4. API PARA CARGA DINÁMICA DE CUESTIONARIOS
# ==========================================================
def lista_cuestionarios(request):
    tipo_id = request.GET.get('tipo_id')
    if tipo_id:
        cuestionarios = list(
            FactCuestionario.objects.filter(tipo_cuestionario_id=tipo_id)
            .values('IdCuestionario', 'NombreCuestionario')
        )
        return JsonResponse({'success': True, 'cuestionarios': cuestionarios})
    return JsonResponse({'success': False, 'cuestionarios': []})
