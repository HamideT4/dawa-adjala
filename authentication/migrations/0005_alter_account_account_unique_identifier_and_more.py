# Generated by Django 4.2.9 on 2024-06-17 14:33

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_transfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_unique_identifier',
            field=models.CharField(default=authentication.models.generate_account_uid, editable=False, max_length=255, unique=True, verbose_name='Numéro du compte'),
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='Solde'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Adresse'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatars/avatar.png', upload_to='avatars/', verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Date de naissance'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Masculin', 'Masculin'), ('Feminin', 'Feminin')], max_length=10, verbose_name='Genre'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Prenom'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=20, null=True, verbose_name='Numero de téléphone'),
        ),
    ]