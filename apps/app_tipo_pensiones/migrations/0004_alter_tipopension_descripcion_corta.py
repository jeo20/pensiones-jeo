# Generated by Django 4.1.5 on 2023-07-19 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tipo_pensiones', '0003_alter_tipopension_codigo_numerico_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipopension',
            name='descripcion_corta',
            field=models.CharField(max_length=4, verbose_name='Descripción corta (4 car.)'),
        ),
    ]
