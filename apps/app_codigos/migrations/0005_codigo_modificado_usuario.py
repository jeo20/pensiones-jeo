# Generated by Django 4.1.5 on 2023-04-10 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_codigos', '0004_alter_codigo_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigo',
            name='modificado_usuario',
            field=models.CharField(default='ADMIN', max_length=30),
        ),
    ]