from Cursos.models import Fact_Curso
from Participante.models import Participante
from django.shortcuts import render

def seleccionar_curso(request, participante_id):
    participante = Participante.objects.get(pk=participante_id)

    # Solo traemos IdCurso y NombreCurso
    cursos = Fact_Curso.objects.all().values('IdCurso', 'NombreCurso')

    mensaje = ""
    if request.method == 'POST':
        curso_id = request.POST.get('curso')
        # Aquí puedes crear la lógica para guardar la inscripción
        mensaje = f"Inscripción registrada para el curso ID {curso_id}"

    context = {
        'participante': participante,
        'cursos': cursos,
        'mensaje': mensaje
    }
    return render(request, 'Participante/seleccionar_curso.html', context)
