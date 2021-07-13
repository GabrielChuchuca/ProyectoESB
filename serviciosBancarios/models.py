from django.db import models

# Create your models here.

class Banco(models.Model):
    nombre = models.CharField(max_length=100)

class Cuenta(models.Model):
    num_cuenta = models.IntegerField()
    monto = models.IntegerField()
    password = models.CharField(max_length=8)
    id_Banco = models.ForeignKey(Banco, null=True, blank=True, on_delete=models.CASCADE)
    #codigobanco

class Transferencia(models.Model):
    fecha_trans = models.DateField()
    tipo_trans = models.CharField(max_length=13)
    id_cuenta = models.ForeignKey(Cuenta, null=True, blank=True, on_delete=models.CASCADE)
    #codigo cuenta

class Cliente(models.Model):
    cedula = models.CharField(max_length=10)
    nombres = models.CharField(max_length=100)
    id_cuenta = models.ForeignKey(Cuenta, null=True, blank=True, on_delete=models.CASCADE)
    #codigocuenta




