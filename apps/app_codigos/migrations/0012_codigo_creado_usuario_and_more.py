# Generated by Django 4.1.5 on 2023-08-02 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_codigos', '0011_codigo_tipo_carga'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigo',
            name='creado_usuario',
            field=models.CharField(default='---', max_length=30),
        ),
        migrations.AlterField(
            model_name='codigo',
            name='modificado_usuario',
            field=models.CharField(default='---', max_length=30),
        ),
    ]