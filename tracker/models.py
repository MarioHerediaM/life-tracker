from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Area(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, default='⭐')
    color = models.CharField(max_length=7, default='#4F8EF7')
    peso = models.PositiveBigIntegerField(default=10)

    def __str__(self):
        return f"{self.emoji} {self.nombre} ({self.usuario.username})"

class Actividad(models.Model):
    PUNTOS_CHOICES= [
        (1, 'Habito'),
        (3, 'Significativo'),
        (5, 'Logro'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    puntos = models.IntegerField(choices=PUNTOS_CHOICES, default=3)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} (+{self.puntos}) - {self.usuario.username}"