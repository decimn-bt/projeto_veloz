from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("estoque", "0002_security_constraints"),
    ]

    operations = [
        migrations.CreateModel(
            name="RegistroConsumo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantidade", models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(__import__("decimal").Decimal("0.01"))])),
                ("unidade", models.CharField(max_length=20)),
                ("estoque_anterior", models.DecimalField(decimal_places=2, max_digits=10)),
                ("estoque_posterior", models.DecimalField(decimal_places=2, max_digits=10)),
                ("registrado_em", models.DateTimeField(auto_now_add=True)),
                ("ingrediente", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="historico_consumos", to="estoque.ingrediente")),
                ("usuario", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="historico_consumos", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-registrado_em"]},
        ),
        migrations.AddConstraint(
            model_name="registroconsumo",
            constraint=models.CheckConstraint(condition=models.Q(quantidade__gt=0), name="registro_consumo_positivo"),
        ),
        migrations.AddConstraint(
            model_name="registroconsumo",
            constraint=models.CheckConstraint(condition=models.Q(estoque_anterior__gte=0), name="registro_estoque_anterior_nao_negativo"),
        ),
        migrations.AddConstraint(
            model_name="registroconsumo",
            constraint=models.CheckConstraint(condition=models.Q(estoque_posterior__gte=0), name="registro_estoque_posterior_nao_negativo"),
        ),
    ]
