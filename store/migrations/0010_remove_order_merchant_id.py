# Generated by Django 5.0.6 on 2024-11-28 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_withdrawalrequest_notes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='merchant_id',
        ),
    ]
