# Generated by Django 5.0.6 on 2024-07-03 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("App_JuriGest", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sentencia",
            name="fecha",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="sentencia",
            name="tipo",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="usuariobase",
            name="tipo",
            field=models.CharField(
                choices=[("juez", "Juez"), ("lector", "Lector")], max_length=20
            ),
        ),
    ]
