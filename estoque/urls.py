from django.urls import path

from .views import consumir_ingrediente, health_check, historico_consumos, lista_compras

urlpatterns = [
    path("", lista_compras, name="lista_compras"),
    path("consumir/<int:ingrediente_id>/", consumir_ingrediente, name="consumir_ingrediente"),
    path("historico/", historico_consumos, name="historico_consumos"),
    path("health/", health_check, name="health_check"),
]
