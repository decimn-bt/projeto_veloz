from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("estoque", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="ingrediente",
            constraint=models.CheckConstraint(
                condition=models.Q(meta__gte=0),
                name="ingrediente_meta_nao_negativa",
            ),
        ),
        migrations.AddConstraint(
            model_name="ingrediente",
            constraint=models.CheckConstraint(
                condition=models.Q(estoque_atual__gte=0),
                name="ingrediente_estoque_nao_negativo",
            ),
        ),
        migrations.AddConstraint(
            model_name="ingrediente",
            constraint=models.CheckConstraint(
                condition=models.Q(consumo_mensal__gte=0),
                name="ingrediente_consumo_nao_negativo",
            ),
        ),
    ]
