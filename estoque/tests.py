from decimal import Decimal

from django.test import TestCase

from .models import Ingrediente
from .services import EstoqueInsuficiente, calcular_compra, registrar_consumo

class CalculoCompraTests(TestCase):
    def criar(self, **kwargs):
        dados = {
            "nome": "Farinha",
            "unidade": "Kg",
            "meta": Decimal("20"),
            "estoque_atual": Decimal("8"),
            "consumo_mensal": Decimal("5"),
        }
        dados.update(kwargs)
        return Ingrediente.objects.create(**dados)

    def test_reposicao_normal(self):
        ingrediente = self.criar()
        self.assertEqual(calcular_compra(ingrediente), Decimal("12.00"))

    def test_consumo_acima_do_estoque_e_da_meta(self):
        ingrediente = self.criar(estoque_atual=Decimal("2"), consumo_mensal=Decimal("25"))
        self.assertEqual(calcular_compra(ingrediente), Decimal("30.00"))

    def test_vencido_compra_meta_completa(self):
        ingrediente = self.criar(estoque_atual=Decimal("8"), vencido=True)
        self.assertEqual(calcular_compra(ingrediente), Decimal("20.00"))

class ConsumoSeguroTests(TestCase):
    def test_consumo_reduz_estoque(self):
        ingrediente = Ingrediente.objects.create(
            nome="Leite",
            unidade="Litro",
            meta=Decimal("20"),
            estoque_atual=Decimal("10"),
            consumo_mensal=Decimal("8"),
        )
        atualizado = registrar_consumo(ingrediente.pk, Decimal("3"))
        self.assertEqual(atualizado.estoque_atual, Decimal("7.00"))

    def test_consumo_maior_que_estoque_e_bloqueado(self):
        ingrediente = Ingrediente.objects.create(
            nome="Ovo",
            unidade="Unidade",
            meta=Decimal("30"),
            estoque_atual=Decimal("2"),
            consumo_mensal=Decimal("2"),
        )
        with self.assertRaises(EstoqueInsuficiente):
            registrar_consumo(ingrediente.pk, Decimal("3"))
        ingrediente.refresh_from_db()
        self.assertEqual(ingrediente.estoque_atual, Decimal("2.00"))
