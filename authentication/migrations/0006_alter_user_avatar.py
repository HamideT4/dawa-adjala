# Generated by Django 4.2.9 on 2024-05-13 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatars/avatar.png', upload_to='avatars/'),
        ),
    ]
