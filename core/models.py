from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Sorteo(models.Model):
    limiteTickets = models.IntegerField(null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, null=True)
    nombrePublico = models.CharField(max_length=50, null=True)
    descripcion = models.TextField(max_length=500, null=True)
    imagen = models.CharField(max_length=500, null=True)
    precioTickets = models.FloatField(null=True)
    fechaSorteo = models.DateTimeField(null=True)

class Ticket(models.Model):
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE)
    ganador = models.BooleanField(default=False)
    nombreComprador = models.CharField(max_length=100, null=True)
    correo = models.CharField(max_length=250, null=True)
    celular = models.CharField(max_length=15, null=True)
    estado = models.BooleanField(default=False)
    fechaVenta = models.DateTimeField(null=True)
    totalPagado = models.FloatField(default=0.00)
    
class Premio(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    descripcion = models.TextField(max_length=500, null=True)
    imagen = models.CharField(max_length=500, null=True)
    
class PremioSorteo(models.Model):
    premio = models.ForeignKey(Premio, on_delete=models.CASCADE)
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE)
