# Generated by Django 4.2.9 on 2024-04-30 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='qr_code',
            field=models.FileField(blank=True, null=True, upload_to='qrcodes/'),
        ),
    ]
