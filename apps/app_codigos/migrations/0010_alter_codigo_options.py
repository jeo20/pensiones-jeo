# Generated by Django 4.1.5 on 2023-08-01 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_codigos', '0009_remove_codigo_observaciones'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='codigo',
            options={'ordering': ['pension', 'codigo_numerico', 'activo', 'modificado']},
        ),
    ]
