# Generated by Django 3.2 on 2023-03-26 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_user_cod'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='cod',
            new_name='key',
        ),
    ]
