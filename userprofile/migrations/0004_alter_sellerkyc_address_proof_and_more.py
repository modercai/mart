# Generated by Django 5.0.6 on 2024-08-15 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_sellerkyc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerkyc',
            name='address_proof',
            field=models.FileField(upload_to='uploads/kyc_documents/address/'),
        ),
        migrations.AlterField(
            model_name='sellerkyc',
            name='id_document',
            field=models.FileField(upload_to='uploads/kyc_documents/id/'),
        ),
    ]