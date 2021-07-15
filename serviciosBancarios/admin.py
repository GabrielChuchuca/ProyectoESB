from django.contrib import admin

# Register your models here.
from serviciosBancarios.models import Cliente, Banco, Cuenta, Transferencia

class ClienteAdmin(admin.ModelAdmin):
    list_display = ("cedula", "nombres", "username", "id_cuenta")

class BancoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)

class CuentaAdmin(admin.ModelAdmin):
    list_display = ("num_cuenta", "monto", "id_Banco")

class TransferenciaAdmin(admin.ModelAdmin):
    list_display = ("fecha_trans", "tipo_trans", "id_cuenta")

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Banco, BancoAdmin)
admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(Transferencia, TransferenciaAdmin)
