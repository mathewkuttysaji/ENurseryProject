# Generated by Django 5.0 on 2023-12-29 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_purchase_address_purchase_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='message',
        ),
    ]
