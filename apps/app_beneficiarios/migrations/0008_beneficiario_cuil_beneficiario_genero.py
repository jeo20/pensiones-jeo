# Generated by Django 4.1.5 on 2023-07-19 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_beneficiarios', '0007_alter_beneficiario_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiario',
            name='cuil',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('X', 'No Binario'), ('N', 'No Delarado')], default='N', max_length=1),
        ),
    ]