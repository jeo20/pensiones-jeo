# Generated by Django 4.1.5 on 2023-08-01 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_beneficiarios', '0009_alter_beneficiario_direccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiario',
            name='creado_usuario',
            field=models.CharField(default='---', max_length=30),
        ),
        migrations.AlterField(
            model_name='beneficiario',
            name='modificado_usuario',
            field=models.CharField(default='---', max_length=30),
        ),
    ]