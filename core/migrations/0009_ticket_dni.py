# Generated by Django 4.2.16 on 2024-12-02 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_raffle_rafflenumber_ticket_codigo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='dni',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
