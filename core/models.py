from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Sorteo(models.Model):
    limiteTickets = models.IntegerField(null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    nombrePublico = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=500)
    imagen = models.CharField(max_length=500)
    precioTickets = models.FloatField(null=False)

class Ticket(models.Model):
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE)
    ganador = models.BooleanField(default=False)
    nombreComprador = models.CharField(max_length=100)
    correo = models.CharField(max_length=250)
    celular = models.CharField(max_length=15)
    estado = models.BooleanField()
class Objeto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=500)
    imagen = models.CharField(max_length=500)
