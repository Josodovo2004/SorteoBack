# Generated by Django 4.2.16 on 2024-11-28 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_ticket_ticketnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raffle',
            name='public_name',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]