# Generated by Django 3.2 on 2021-04-14 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neige_soleil_app', '0003_delete_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='is_proprietaire',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
