from django.urls import path
from . import views

app_name = 'encuestas'

urlpatterns = [
    # Ruta principal para seleccionar encuesta y curso
    path('', views.seleccionar_encuesta, name='seleccionar_encuesta'),
    
    # Formulario para responder el cuestionario seleccionado
    path('responder/<int:id_cuestionario>/<int:id_curso>/', views.responder_encuesta, name='responder_encuesta'),
    
    # Confirmación de envío exitoso
    path('exitosa/', views.encuesta_exitosa, name='encuesta_exitosa'),
    
    # API JSON para combos dinámicos
    path('api/cuestionarios/', views.lista_cuestionarios, name='lista_cuestionarios'),
]
