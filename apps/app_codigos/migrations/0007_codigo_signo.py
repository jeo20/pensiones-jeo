# Generated by Django 4.1.5 on 2023-07-31 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_codigos', '0006_alter_codigo_calculo_alter_codigo_codigo_numerico_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigo',
            name='signo',
            field=models.CharField(choices=[('P', 'SUMA'), ('N', 'RESTA')], default='P', max_length=1),
        ),
    ]
