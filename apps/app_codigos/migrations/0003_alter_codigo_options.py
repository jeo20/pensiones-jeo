# Generated by Django 4.1.5 on 2023-01-27 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_codigos', '0002_alter_codigo_calculo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='codigo',
            options={'ordering': ['codigo_numerico', 'activo']},
        ),
    ]