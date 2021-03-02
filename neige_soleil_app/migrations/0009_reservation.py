# Generated by Django 3.1.4 on 2021-02-18 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neige_soleil_app', '0008_auto_20210217_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reservation', models.DateField(auto_now_add=True)),
                ('date_debut_sejour', models.DateField()),
                ('date_fin_sejour', models.DateField()),
                ('status_reservation', models.CharField(choices=[('WAIT', 'En cours'), ('VALID', 'Confirmer'), ('CANCEL', 'Annuler')], default='WAIT', max_length=6)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neige_soleil_app.contratproprietaire')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neige_soleil_app.profile')),
            ],
        ),
    ]