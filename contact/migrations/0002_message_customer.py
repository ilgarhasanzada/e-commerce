# Generated by Django 4.1.4 on 2023-01-01 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='account.customer'),
        ),
    ]
