from django.db import models
from Cursos.models import Fact_Curso

# ==========================================================
# DIMENSIONES
# ==========================================================

class DimTipoCuestionario(models.Model):
    IdTipoCuestionario = models.IntegerField(primary_key=True, db_column='IdTipoCuestionario')
    NombreTipoCuestionario = models.CharField(max_length=200, db_column='NombreTipoCuestionario')

    class Meta:
        managed = False
        db_table = 'Dim_TipoCuestionario'

    def __str__(self):
        return self.NombreTipoCuestionario


class DimTipoPregunta(models.Model):
    IdTipoPregunta = models.IntegerField(primary_key=True, db_column='IdTipoPregunta')
    NombreTipoPregunta = models.CharField(max_length=200, db_column='NombreTipoPregunta')

    class Meta:
        managed = False
        db_table = 'Dim_TipoPregunta'

    def __str__(self):
        return self.NombreTipoPregunta


# ==========================================================
# HECHOS (FACTS) Y ESTRUCTURA DE CUESTIONARIOS
# ==========================================================

class FactCuestionario(models.Model):
    IdCuestionario = models.IntegerField(primary_key=True, db_column='IdCuestionario')
    NombreCuestionario = models.CharField(max_length=500, db_column='NombreCuestionario')
    tipo_cuestionario = models.ForeignKey(
        DimTipoCuestionario, 
        on_delete=models.DO_NOTHING, 
        db_column='IdTipoCuestionario'
    )

    class Meta:
        managed = False
        db_table = 'Fact_Cuestionario'

    def __str__(self):
        return self.NombreCuestionario


class FactSubPregunta(models.Model):
    IdSubPregunta = models.IntegerField(primary_key=True, db_column='IdSubPregunta')
    NombreSubPregunta = models.CharField(max_length=500, db_column='NombreSubPregunta')
    tipo_pregunta = models.ForeignKey(
        DimTipoPregunta, 
        on_delete=models.DO_NOTHING, 
        db_column='IdTipoPregunta'
    )

    class Meta:
        managed = False
        db_table = 'Fact_SubPregunta'

    def __str__(self):
        return self.NombreSubPregunta


class FactPregunta(models.Model):
    IdPregunta = models.IntegerField(primary_key=True, db_column='IdPregunta')
    NombrePregunta = models.CharField(max_length=500, db_column='NombrePregunta')
    tipo_pregunta = models.ForeignKey(
        DimTipoPregunta, 
        on_delete=models.DO_NOTHING, 
        db_column='IdTipoPregunta'
    )
    sub_pregunta = models.ForeignKey(
        FactSubPregunta, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        db_column='IdSubPregunta'
    )

    class Meta:
        managed = False
        db_table = 'Fact_Pregunta'

    def __str__(self):
        return self.NombrePregunta


class FactRespuestaCuestionario(models.Model):
    IdRespuestaCuestionario = models.AutoField(primary_key=True, db_column='IdRespuestaCuestionario')
    pregunta = models.ForeignKey(
        FactPregunta, 
        on_delete=models.DO_NOTHING, 
        db_column='IdPregunta'
    )
    cuestionario = models.ForeignKey(
        FactCuestionario, 
        on_delete=models.DO_NOTHING, 
        db_column='IdCuestionario'
    )
    
    # Campo de participante que será null dado que la encuesta es anónima
    IdParticipante = models.CharField(max_length=10, db_column='IdParticipante', null=True, blank=True)
    
    # Curso asociado
    curso = models.ForeignKey(
        Fact_Curso, 
        on_delete=models.DO_NOTHING, 
        db_column='IdCurso'
    )
    
    # Modulo (puede ser null para evaluaciones generales)
    IdModulo = models.IntegerField(db_column='IdModulo', null=True, blank=True)
    
    FechaRespuesta = models.DateField(db_column='FechaRespuesta')
    Respuesta = models.CharField(max_length=120, db_column='Respuesta')

    class Meta:
        managed = False
        db_table = 'Fact_RespuestaCuestionario'

    def __str__(self):
        return f"Respuesta a Pregunta {self.pregunta_id} - Cuestionario {self.cuestionario_id}"
