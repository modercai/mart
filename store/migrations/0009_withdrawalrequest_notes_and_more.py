# Generated by Django 5.0.6 on 2024-11-24 17:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_withdrawalrequest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawalrequest',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawal_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='VendorBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pending_withdrawal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('vendor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_balance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
