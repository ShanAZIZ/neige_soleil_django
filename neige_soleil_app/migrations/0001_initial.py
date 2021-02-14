# Generated by Django 3.1.4 on 2021-02-13 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description_breve', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=1000)),
                ('surface_habitable', models.FloatField()),
                ('surface_balcon', models.FloatField()),
                ('capacite', models.IntegerField()),
                ('distance_pistes', models.FloatField()),
                ('status', models.CharField(choices=[('AVAIL', 'Disponible'), ('BUSY', 'Occuper'), ('OFF', 'Inactif')], default='AVAIL', max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adresse', models.CharField(max_length=200)),
                ('code_postale', models.IntegerField()),
                ('ville', models.CharField(max_length=200)),
                ('telephone', models.IntegerField()),
                ('rib', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LocationsImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locations', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neige_soleil_app.location')),
            ],
        ),
    ]
