from decimal import Decimal
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('unidade', models.CharField(choices=[('Kg', 'Kg'), ('Litro', 'Litro'), ('Unidade', 'Unidade'), ('g', 'g'), ('ml', 'ml')], max_length=20)),
                ('meta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estoque_atual', models.DecimalField(decimal_places=2, max_digits=10)),
                ('consumo_mensal', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('vencido', models.BooleanField(default=False)),
                ('faltou_no_mes', models.BooleanField(default=False)),
            ],
            options={'ordering': ['nome']},
        ),
    ]
