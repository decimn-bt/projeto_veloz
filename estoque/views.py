from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import Ingrediente, RegistroConsumo
from .services import ConsumoInvalido, EstoqueInsuficiente, gerar_lista_compras, registrar_consumo


@require_GET
def lista_compras(request):
    query = request.GET.get("q", "").strip()[:100]
    ingredientes = Ingrediente.objects.all()

    if query:
        ingredientes = ingredientes.filter(nome__icontains=query)

    compras = gerar_lista_compras(ingredientes)

    return render(
        request,
        "estoque/lista_compras.html",
        {
            "compras": compras,
            "ingredientes": ingredientes,
            "query": query,
        },
    )


@staff_member_required
@require_POST
def consumir_ingrediente(request, ingrediente_id):
    valor = request.POST.get("quantidade", "").strip()

    try:
        quantidade = Decimal(valor)
    except (InvalidOperation, ValueError):
        messages.error(request, "Informe uma quantidade válida.")
        return redirect("lista_compras")

    try:
        ingrediente = registrar_consumo(ingrediente_id, quantidade, request.user)
    except Ingrediente.DoesNotExist:
        messages.error(request, "Ingrediente não encontrado.")
        return redirect("lista_compras")
    except ConsumoInvalido:
        messages.error(request, "A quantidade de consumo deve ser maior que zero.")
        return redirect("lista_compras")
    except EstoqueInsuficiente:
        messages.error(request, "O consumo informado não pode ser maior que o estoque atual.")
        return redirect("lista_compras")

    messages.success(
        request,
        f"Consumo registrado. Estoque de {ingrediente.nome}: {ingrediente.estoque_atual} {ingrediente.unidade}.",
    )
    return redirect("lista_compras")


@staff_member_required
@require_GET
def historico_consumos(request):
    query = request.GET.get("q", "").strip()[:100]
    historico = RegistroConsumo.objects.select_related("ingrediente", "usuario")

    if query:
        historico = historico.filter(
            Q(ingrediente__nome__icontains=query)
            | Q(usuario__username__icontains=query)
        )

    return render(
        request,
        "estoque/historico.html",
        {
            "historico": historico[:200],
            "query": query,
        },
    )


@require_GET
def health_check(request):
    return JsonResponse({"status": "ok"})
