from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Habitacion(models.Model):
    numero = models.IntegerField()
    tipo = models.CharField(max_length=30)
    disponible = models.BooleanField()   

    def __str__(self):
        return f'{self.numero}'    

class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    documento = models.IntegerField()
    email = models.EmailField(max_length=30)

    def __str__(self):
        return f'{self.nombre}'
    
class Empleado(models.Model):
    nombre = models.CharField(max_length=50)
    documento = models.IntegerField()
    email = models.EmailField(max_length=30)
    puesto = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nombre}'

class Reserva(models.Model):
    estado = models.BooleanField()
    fechainicio = models.DateField()
    fechafin = models.DateField()
    
    def __str__(self):
        return f'{Cliente.nombre} - {Habitacion.numero} - {self.estado} Desde {self.fechainicio} Hasta {self.fechafin}'


    
class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)

