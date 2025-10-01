from django.urls import path
from . import views

app_name = 'participante'  # 🔹 Añadido para usar namespace en redirect

urlpatterns = [
    # Vista clásica de búsqueda/registro de participante
    path('', views.buscar_participante, name='buscar_participante'),

    # Selección de curso tras registrar o actualizar participante
    path('seleccionar_curso/<int:id_participante>/', views.seleccionar_curso, name='seleccionar_curso'),

    # Endpoints JSON para participantes
    path('api/buscar/', views.buscar_participante_json, name='buscar_participante_json'),
    path('api/registrar/', views.registrar_participante_json, name='registrar_participante_json'),

    # Endpoints JSON para combos dependientes (cascada)
    path('api/paises/', views.lista_paises, name='lista_paises'),
    path('api/departamentos/', views.lista_departamentos, name='lista_departamentos'),
    path('api/provincias/', views.lista_provincias, name='lista_provincias'),
    path('api/distritos/', views.lista_distritos, name='lista_distritos'),
]
