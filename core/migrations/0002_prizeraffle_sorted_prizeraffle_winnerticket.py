# Generated by Django 5.1.3 on 2024-11-25 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prizeraffle',
            name='sorted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prizeraffle',
            name='winnerTicket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.ticket'),
        ),
    ]