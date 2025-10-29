# app_cliente/models.py

from django.db import models

class Cliente(models.Model):
    # Django creará automáticamente un campo 'id' como Primary Key
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Perro(models.Model):
    # Django creará automáticamente un campo 'id' como Primary Key
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    temperamento = models.TextField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='perros')
    foto = models.ImageField(upload_to='perros_fotos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.raza}) - Cliente: {self.cliente.nombre}"