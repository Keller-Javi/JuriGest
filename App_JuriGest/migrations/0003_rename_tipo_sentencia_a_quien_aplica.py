# Generated by Django 5.0.6 on 2024-07-04 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("App_JuriGest", "0002_alter_sentencia_fecha_alter_sentencia_tipo_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="sentencia",
            old_name="tipo",
            new_name="a_quien_aplica",
        ),
    ]
