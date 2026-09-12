from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Ingrediente(models.Model):
    UNIDADES = [
        ("Kg", "Kg"),
        ("Litro", "Litro"),
        ("Unidade", "Unidade"),
        ("g", "g"),
        ("ml", "ml"),
    ]

    nome = models.CharField(max_length=100)
    unidade = models.CharField(max_length=20, choices=UNIDADES)
    meta = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    estoque_atual = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    consumo_mensal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"), validators=[MinValueValidator(Decimal("0"))])
    vencido = models.BooleanField(default=False)
    faltou_no_mes = models.BooleanField(default=False)

    class Meta:
        ordering = ["nome"]
        constraints = [
            models.CheckConstraint(condition=models.Q(meta__gte=0), name="ingrediente_meta_nao_negativa"),
            models.CheckConstraint(condition=models.Q(estoque_atual__gte=0), name="ingrediente_estoque_nao_negativo"),
            models.CheckConstraint(condition=models.Q(consumo_mensal__gte=0), name="ingrediente_consumo_nao_negativo"),
        ]

    def __str__(self):
        return self.nome


class RegistroConsumo(models.Model):
    ingrediente = models.ForeignKey(
        Ingrediente,
        on_delete=models.PROTECT,
        related_name="historico_consumos",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="historico_consumos",
    )
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    unidade = models.CharField(max_length=20)
    estoque_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_posterior = models.DecimalField(max_digits=10, decimal_places=2)
    registrado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-registrado_em"]
        constraints = [
            models.CheckConstraint(condition=models.Q(quantidade__gt=0), name="registro_consumo_positivo"),
            models.CheckConstraint(condition=models.Q(estoque_anterior__gte=0), name="registro_estoque_anterior_nao_negativo"),
            models.CheckConstraint(condition=models.Q(estoque_posterior__gte=0), name="registro_estoque_posterior_nao_negativo"),
        ]

    def __str__(self):
        return f"{self.ingrediente.nome} - {self.quantidade} {self.unidade}"
