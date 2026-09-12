from django import forms

from .models import Ingrediente

class IngredienteAdminForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = [
            "nome",
            "unidade",
            "meta",
            "estoque_atual",
            "consumo_mensal",
            "vencido",
            "faltou_no_mes",
        ]
