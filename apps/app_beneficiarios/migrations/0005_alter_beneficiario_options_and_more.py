# Generated by Django 4.1.5 on 2023-04-10 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ubicacion', '0002_alter_ubicacion_localidad'),
        ('app_beneficiarios', '0004_rename_tipo_doc_beneficiario_documento_tipo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='beneficiario',
            options={'ordering': ['ubicacion', 'legajo', 'tipo_pension']},
        ),
        migrations.AlterIndexTogether(
            name='beneficiario',
            index_together={('ubicacion', 'legajo')},
        ),
        migrations.AddIndex(
            model_name='beneficiario',
            index=models.Index(fields=['apellido_y_nombre'], name='app_benefic_apellid_1f1674_idx'),
        ),
        migrations.AddIndex(
            model_name='beneficiario',
            index=models.Index(fields=['documento'], name='app_benefic_documen_14905f_idx'),
        ),
        migrations.AddIndex(
            model_name='beneficiario',
            index=models.Index(fields=['tipo_pension'], name='app_benefic_tipo_pe_4b9725_idx'),
        ),
    ]
