from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    celular = models.CharField(max_length=15)

class Sorteo(models.Model):
    limiteTickets = models.IntegerField(null=False)
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class Ticket(models.Model):
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    precio = models.FloatField(null=False)
    ganador = models.BooleanField(default=False)

class Objeto(models.Model):
    nombre = models.CharField(max_length=200)
    imagen = models.ImageField()
