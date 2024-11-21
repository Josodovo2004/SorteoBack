from django.db import models
from django.contrib.auth.models import User

class Raffle(models.Model):
    ticket_limit = models.IntegerField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    public_name = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=500, null=True)
    image = models.CharField(max_length=500, null=True)
    ticket_price = models.FloatField(null=True)
    raffle_date = models.DateTimeField(null=True)

class Ticket(models.Model):
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    is_winner = models.BooleanField(default=False)
    buyer_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=250, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    status = models.BooleanField(default=False)
    sale_date = models.DateTimeField(null=True)
    total_paid = models.FloatField(default=0.00)

class Prize(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=500, null=True)
    image = models.CharField(max_length=500, null=True)

class PrizeRaffle(models.Model):
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
