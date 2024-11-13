# Generated by Django 4.1.5 on 2023-08-02 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_codigos', '0010_alter_codigo_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigo',
            name='tipo_carga',
            field=models.CharField(choices=[('U', 'Carga Manual'), ('M', 'Carga Masiva desde Archivo'), ('A', 'Carga a través de API')], default='U', max_length=1),
        ),
    ]
