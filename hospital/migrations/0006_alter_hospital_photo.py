# Generated by Django 4.2.9 on 2024-02-19 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_alter_hospital_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='photo',
            field=models.ImageField(upload_to='hospital_photos/'),
        ),
    ]
