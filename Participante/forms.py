from django import forms
from .models import (
    Participante, Pais, Departamento, Provincia, Distrito,
    Profesion, GradoInstruccion, CentroEstudio, TipoCentroEstudio,
    Origen, TipoDocumento
)

class ParticipanteForm(forms.ModelForm):
    # 🔹 Campo desplegable de hora de contacto
    HORAS_CHOICES = [(str(h), f"{h}:00") for h in range(7, 24)]
    HoraContactoParticipante = forms.ChoiceField(
        choices=HORAS_CHOICES,
        required=False,
        label="Hora de contacto"
    )

    class Meta:
        model = Participante
        fields = [
            'tipo_documento', 'dni',
            'nombres', 'apellido_paterno', 'apellido_materno',
            'fecha_nacimiento', 'direccion', 'centro_trabajo',
            'email_principal', 'email_secundario', 'celular', 'telefono_fijo',
            'pais', 'departamento', 'provincia', 'distrito',
            'profesion', 'grado_instruccion', 'centro_estudio', 'tipo_centro_estudio',
            'origen',
            'HoraContactoParticipante',  # 🔹 agregamos aquí también
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔹 Cargar todos los selects normales
        self.fields['tipo_documento'].queryset = TipoDocumento.objects.all()
        self.fields['profesion'].queryset = Profesion.objects.all()
        self.fields['grado_instruccion'].queryset = GradoInstruccion.objects.all()
        self.fields['centro_estudio'].queryset = CentroEstudio.objects.all()
        self.fields['tipo_centro_estudio'].queryset = TipoCentroEstudio.objects.all()
        self.fields['origen'].queryset = Origen.objects.all()

        # 🔹 Cargar cascada inicial
        self.fields['pais'].queryset = Pais.objects.all()
        self.fields['departamento'].queryset = Departamento.objects.none()
        self.fields['provincia'].queryset = Provincia.objects.none()
        self.fields['distrito'].queryset = Distrito.objects.none()

        # 🔹 Si estoy editando, mostrar jerarquía correcta
        if self.instance and self.instance.pais:
            self.fields['departamento'].queryset = Departamento.objects.filter(pais=self.instance.pais)
        if self.instance and self.instance.departamento:
            self.fields['provincia'].queryset = Provincia.objects.filter(departamento=self.instance.departamento)
        if self.instance and self.instance.provincia:
            self.fields['distrito'].queryset = Distrito.objects.filter(provincia=self.instance.provincia)
