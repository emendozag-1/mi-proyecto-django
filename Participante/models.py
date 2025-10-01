from django.db import models

# ==============================
# MODELOS DE DIMENSIONES
# ==============================

class Pais(models.Model):
    id = models.AutoField(primary_key=True, db_column='IdPais')
    nombre = models.CharField(max_length=40, db_column='NombrePais')

    class Meta:
        managed = False
        db_table = 'Dim_Pais'

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='IdDepartamento')
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, db_column='IdPais')
    nombre = models.CharField(max_length=40, db_column='NombreDepartamento')

    class Meta:
        managed = False
        db_table = 'Dim_Departamento'

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    id = models.AutoField(primary_key=True, db_column='IdProvincia')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, db_column='IdDepartamento')
    nombre = models.CharField(max_length=40, db_column='NombreProvincia')

    class Meta:
        managed = False
        db_table = 'Dim_Provincia'

    def __str__(self):
        return self.nombre


class Distrito(models.Model):
    id = models.AutoField(primary_key=True, db_column='IdDistrito')
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, db_column='IdProvincia')
    nombre = models.CharField(max_length=40, db_column='NombreDistrito')

    class Meta:
        managed = False
        db_table = 'Dim_Distrito'

    def __str__(self):
        return self.nombre


class Origen(models.Model):
    id = models.AutoField(primary_key=True, db_column='IdOrigen')
    nombre = models.CharField(max_length=20, db_column='NombreOrigen')

    class Meta:
        managed = False
        db_table = 'Dim_Origen'

    def __str__(self):
        return self.nombre


class TipoDocumento(models.Model):
    id = models.AutoField(primary_key=True, db_column='IdTipoDocumento')
    nombre = models.CharField(max_length=40, db_column='NombreTipoDocumento')
    codigo = models.CharField(max_length=5, db_column='CodigoTipoDocumento')

    class Meta:
        managed = False
        db_table = 'Dim_TipoDocumento'

    def __str__(self):
        return self.nombre


class Profesion(models.Model):
    id = models.AutoField(primary_key=True, db_column='IdProfesion')
    nombre = models.CharField(max_length=90, db_column='NombreProfesion')

    class Meta:
        managed = False
        db_table = 'Dim_Profesion'

    def __str__(self):
        return self.nombre


class GradoInstruccion(models.Model):
    id = models.AutoField(primary_key=True, db_column='IdGradoInstruccion')
    nombre = models.CharField(max_length=25, db_column='NombreGradoInstruccion')

    class Meta:
        managed = False
        db_table = 'Dim_GradoInstruccion'

    def __str__(self):
        return self.nombre


class CentroEstudio(models.Model):
    id = models.AutoField(primary_key=True, db_column='IdCentroEstudio')
    nombre = models.CharField(max_length=80, db_column='NombreCentroEstudio')
    tipo_gestion = models.CharField(max_length=10, db_column='TipoGestionCentroEstudio')

    class Meta:
        managed = False
        db_table = 'Dim_CentroEstudio'

    def __str__(self):
        return self.nombre


class TipoCentroEstudio(models.Model):
    id = models.AutoField(primary_key=True, db_column='IdTipoCentroEstudio')
    nombre = models.CharField(max_length=20, db_column='NombreTipoCentroEstudio')

    class Meta:
        managed = False
        db_table = 'Dim_TipoCentroEstudio'

    def __str__(self):
        return self.nombre


# ==============================
# MODELO PARTICIPANTE
# ==============================

class Participante(models.Model):
    id = models.AutoField(primary_key=True, db_column='Id')
    dni = models.CharField(max_length=25, db_column='DocumentoParticipante')
    nombres = models.CharField(max_length=40, db_column='NombresParticipante')
    apellido_paterno = models.CharField(max_length=20, db_column='ApellidoPaternoParticipante')
    apellido_materno = models.CharField(max_length=20, db_column='ApellidoMaternoParticipante')
    fecha_nacimiento = models.DateField(db_column='FechaNacimientoParticipante', null=True, blank=True)
    direccion = models.CharField(max_length=60, db_column='DireccionParticipante', null=True, blank=True)
    centro_trabajo = models.CharField(max_length=40, db_column='CentroTrabajoParticipante', null=True, blank=True)
    email_principal = models.CharField(max_length=50, db_column='EmailPrincipalParticipante', null=True, blank=True)
    email_secundario = models.CharField(max_length=50, db_column='EmailSecundarioParticipante', null=True, blank=True)
    celular = models.CharField(max_length=12, db_column='CelularParticipante', null=True, blank=True)
    telefono_fijo = models.CharField(max_length=12, db_column='TelefonoFijoParticipante', null=True, blank=True)
    HoraContactoParticipante = models.CharField(max_length=2, null=True, blank=True)

    # 🔹 Relaciones con tablas dimensionales
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdPais')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdDepartamento')
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdProvincia')
    distrito = models.ForeignKey(Distrito, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdDistrito')
    profesion = models.ForeignKey(Profesion, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdProfesion')
    grado_instruccion = models.ForeignKey(GradoInstruccion, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdGradoInstruccion')
    centro_estudio = models.ForeignKey(CentroEstudio, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdCentroEstudio')
    tipo_centro_estudio = models.ForeignKey(TipoCentroEstudio, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdTipoCentroEstudio')
    origen = models.ForeignKey(Origen, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdOrigen')
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdTipoDocumento')

    # 🔹 Defaults
    spam = models.IntegerField(default=1, db_column='SpamParticipante')
    usuario_registro = models.CharField(max_length=100, default="Formulario Web", db_column='UsuarioRegistroParticipante')
    fecha_registro = models.DateField(auto_now=True, db_column='FechaRegistroParticipante')

    class Meta:
        managed = False
        db_table = 'Fact_Participante'

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno} ({self.dni})"
