from django.contrib import admin

from .forms import IngredienteAdminForm
from .models import Ingrediente, RegistroConsumo


@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    form = IngredienteAdminForm
    list_display = (
        "nome",
        "unidade",
        "meta",
        "estoque_atual",
        "consumo_mensal",
        "vencido",
        "faltou_no_mes",
    )
    list_filter = ("unidade", "vencido", "faltou_no_mes")
    search_fields = ("nome",)
    list_per_page = 50


@admin.register(RegistroConsumo)
class RegistroConsumoAdmin(admin.ModelAdmin):
    list_display = (
        "ingrediente",
        "quantidade",
        "unidade",
        "estoque_anterior",
        "estoque_posterior",
        "usuario",
        "registrado_em",
    )
    list_filter = ("unidade", "registrado_em")
    search_fields = ("ingrediente__nome", "usuario__username")
    readonly_fields = (
        "ingrediente",
        "usuario",
        "quantidade",
        "unidade",
        "estoque_anterior",
        "estoque_posterior",
        "registrado_em",
    )
    ordering = ("-registrado_em",)
    list_per_page = 50
