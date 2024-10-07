from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class UsuarioBase(AbstractUser):
    TIPO_CHOICES = [
        ('juez', 'Juez'),
        ('lector', 'Lector')]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)  # 'juez' o 'lector'

    class Meta:
        db_table = 'usuario_base'

class Juez(UsuarioBase):
    matricula = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - Juez"

class Lector(UsuarioBase):
    id_usuario = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - Lector"

class Sentencia(models.Model):
    id_sentencia = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    a_quien_aplica = models.CharField(max_length=300)
    fecha = models.DateTimeField(auto_now_add=False) # Se añade la fecha al momento de crear la instancia

    REVISTA_O_PROVINCIAL_CHOICES = [
        ('Revista', 'Revista'),
        ('Provincial', 'Provincial'),
    ]

    INSTANCIA_CHOICES = [
        ('Primer instancia', 'Primer instancia'),
        ('Segunda instancia', 'Segunda instancia'),
        ('Tercera instancia', 'Tercera instancia'),
    ]

    revista_o_provincial = models.CharField(max_length=10, choices=REVISTA_O_PROVINCIAL_CHOICES)
    instancia = models.CharField(max_length=20, choices=INSTANCIA_CHOICES)

    user = models.ForeignKey(UsuarioBase, on_delete=models.CASCADE) # Esto no debería estar, en caso de que se elimine un juez, no debería limpiar sus sentencias

    def __str__(self):
        return self.titulo

class Doctrina(models.Model):
    id_doctrina = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True) # Se añade la fecha al momento de crear la instancia
    autor = models.CharField(max_length=100)
    revista_juridica = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo