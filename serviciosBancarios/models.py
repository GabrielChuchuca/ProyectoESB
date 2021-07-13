from django.db import models

# Create your models here.

class Banco(models.Model):
    nombre = models.CharField(max_length=100)

class Cuenta(models.Model):
    num_cuenta = models.IntegerField()
    monto = models.IntegerField()
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
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=8)
    id_cuenta = models.ForeignKey(Cuenta, null=True, blank=True, on_delete=models.CASCADE)

    #def __str__(self):
    #    return self.nombres
    #codigocuenta

    """def validar_login(self, username="", password=""):
        result = Cliente.objects.filter(username__icontains=username, password__icontains=password)
        if result:
            print("QUI OE", result)
            return result[0]
        else:
            return False"""




