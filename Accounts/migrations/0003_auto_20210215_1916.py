# Generated by Django 3.1.3 on 2021-02-15 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='cart_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='post_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='province',
        ),
    ]
