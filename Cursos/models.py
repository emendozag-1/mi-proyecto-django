from django.db import models


# ==========================================================
# TABLA: Fact_Curso
# ==========================================================
class Fact_Curso(models.Model):
    IdCurso = models.AutoField(primary_key=True)
    IdFormato = models.IntegerField(null=True, blank=True)
    IdModalidad = models.IntegerField(null=True, blank=True)
    IdProveedor = models.IntegerField(null=True, blank=True)
    IdConceptoPago = models.IntegerField(null=True, blank=True)
    IdTipoEntidad = models.IntegerField(null=True, blank=True)
    IdEntidad = models.IntegerField(null=True, blank=True)
    IdPonente = models.CharField(max_length=8, null=True, blank=True)
    NombreCurso = models.CharField(max_length=200)
    ConfirmacionInHouseCurso = models.IntegerField(null=True, blank=True)
    FechaCoordinacionCurso = models.DateField(null=True, blank=True)
    FechaRequerimientoCurso = models.DateField(null=True, blank=True)
    FechaAperturaCurso = models.DateField(null=True, blank=True)
    FechaFinalizacionCurso = models.DateField(null=True, blank=True)
    FechaCierreCurso = models.DateField(null=True, blank=True)
    MontoCurso = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    EnlaceModeloCurso = models.CharField(max_length=700, null=True, blank=True)
    ResolucionCurso = models.CharField(max_length=500, null=True, blank=True)
    EnlaceResolucionCurso = models.CharField(max_length=500, null=True, blank=True)
    FechaEnvioCertificadoCurso = models.DateField(null=True, blank=True)
    PonenteEmitioReciboCurso = models.CharField(max_length=2, null=True, blank=True)
    PonenteCumplioMetaCurso = models.CharField(max_length=2, null=True, blank=True)
    CanceladoCurso = models.IntegerField(null=True, blank=True)
    SitioWebCurso = models.IntegerField(default=0)
    ImagenSitioWebCurso = models.TextField(null=True, blank=True)
    UsuarioRegistroCurso = models.CharField(max_length=100, null=True, blank=True)
    FechaRegistroCurso = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.NombreCurso

    class Meta:
        db_table = 'Fact_Curso'  # nombre exacto en SQL Server
        managed = False          # 🔹 importante si ya existe la tabla


# ==========================================================
# TABLA: Fact_Inscripcion
# ==========================================================
class Fact_Inscripcion(models.Model):
    IdInscripcion = models.AutoField(primary_key=True)
    IdParticipante = models.CharField(max_length=10)
    IdCurso = models.IntegerField()
    IdEstadoEntregaAcreditacion = models.IntegerField(default=2)
    IdEstadoInscripcion = models.IntegerField(default=1)
    IdModalidad = models.IntegerField(null=True, blank=True)  # 🔹 agregado
    MotivoParticipacionInscripcion = models.CharField(max_length=300, null=True, blank=True)
    ObservacionCertificadoInscripcion = models.CharField(max_length=300, null=True, blank=True)
    FechaEnviarCertificadoInscripcion = models.DateField(null=True, blank=True)
    FechaEnvioCertificadoInscripcion = models.DateField(null=True, blank=True)
    BecaCompletaInscripcion = models.IntegerField(default=0)
    UsuarioRegistroInscripcion = models.CharField(max_length=100, null=True, blank=True)
    FechaInscripcion = models.DateField(null=True, blank=True)  # 👈 debe ser Date, no DateTime
    DeseaCertificadoInscripcion = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.IdParticipante} - {self.IdCurso}"

    class Meta:
        db_table = 'Fact_Inscripcion'
        managed = False  # 🔹 la tabla ya existe en SQL Server


# ==========================================================
# TABLA: Dim_Modalidad
# ==========================================================
class Dim_Modalidad(models.Model):
    IdModalidad = models.IntegerField(primary_key=True)
    NombreModalidad = models.CharField(max_length=20)
    CodigoModalidad = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.NombreModalidad

    class Meta:
        db_table = 'Dim_Modalidad'
        managed = False  # 🔹 la tabla ya existe en SQL Server
