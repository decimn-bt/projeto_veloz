from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction

from .models import Ingrediente, RegistroConsumo


class ConsumoInvalido(Exception):
    pass


class EstoqueInsuficiente(Exception):
    pass


def calcular_compra(ingrediente):
    meta = ingrediente.meta
    estoque = ingrediente.estoque_atual
    consumo = ingrediente.consumo_mensal

    consumo_superou_estoque_e_meta = consumo > estoque and consumo > meta

    if ingrediente.vencido:
        quantidade = meta
    elif ingrediente.faltou_no_mes or consumo_superou_estoque_e_meta:
        quantidade = consumo * Decimal("1.20")
    else:
        quantidade = meta - estoque

    return quantidade.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def gerar_lista_compras(ingredientes):
    lista = []

    for ingrediente in ingredientes:
        quantidade = calcular_compra(ingrediente)

        if quantidade > 0:
            lista.append({
                "ingrediente": ingrediente.nome,
                "quantidade": quantidade,
                "unidade": ingrediente.unidade,
            })

    return lista


@transaction.atomic
def registrar_consumo(ingrediente_id, quantidade, usuario=None):
    if quantidade <= 0:
        raise ConsumoInvalido

    ingrediente = Ingrediente.objects.select_for_update().get(pk=ingrediente_id)

    atualizado = Ingrediente.objects.filter(
        pk=ingrediente.pk,
        estoque_atual__gte=quantidade,
    ).update(
        estoque_atual=ingrediente.estoque_atual - quantidade,
        consumo_mensal=ingrediente.consumo_mensal + quantidade,
    )

    if atualizado == 0:
        raise EstoqueInsuficiente

    estoque_posterior = ingrediente.estoque_atual - quantidade

    RegistroConsumo.objects.create(
        ingrediente=ingrediente,
        usuario=usuario,
        quantidade=quantidade,
        unidade=ingrediente.unidade,
        estoque_anterior=ingrediente.estoque_atual,
        estoque_posterior=estoque_posterior,
    )

    ingrediente.estoque_atual = estoque_posterior
    ingrediente.consumo_mensal += quantidade
    return ingrediente
