# Generated by Django 5.1.7 on 2025-03-21 23:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_ship_table_alter_shipcategory_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='nave',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ship'),
        ),
        migrations.DeleteModel(
            name='Nave',
        ),
    ]
