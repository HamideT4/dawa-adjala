# Generated by Django 4.2.9 on 2024-02-09 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='uid',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]