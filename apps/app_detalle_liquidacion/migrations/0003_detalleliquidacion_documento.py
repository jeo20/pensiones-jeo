# Generated by Django 4.1.5 on 2023-04-11 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_detalle_liquidacion', '0002_detalleliquidacion_recibo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleliquidacion',
            name='documento',
            field=models.PositiveIntegerField(default=1),
        ),
    ]