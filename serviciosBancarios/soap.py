from django.views.decorators.csrf import csrf_exempt
from spyne.application import Application
from spyne.decorator import rpc
from spyne.model.primitive import Unicode, Integer, String, DateTime, AnyDict
from spyne.model.primitive.number import Double
from spyne.protocol.soap import Soap11
from spyne.server import django
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase
import json

from spyne import Iterable, Array, AnyDict
from spyne import ComplexModel
from django.forms.models import model_to_dict

from django.db import IntegrityError
from spyne.error import ResourceNotFoundError
from spyne.model.fault import Fault
from django.db.models.deletion import ProtectedError
from serviciosBancarios.models import Banco, Cliente, Transferencia, Cuenta
import datetime
from django.http.response import JsonResponse

class Mensaje(ComplexModel):
    cedula = String
    nombres = String
    username = String
    id_cuenta = String
    num_cuenta = Integer
    monto = Integer
    id_trans = Integer
    fecha_trans = DateTime
    tipo_trans = String
    Banco = String 

class Cuentas(ComplexModel):
    num_cuenta = Integer
    monto = Integer
    #id_Banco = String


class SoapService(ServiceBase):
    @rpc(Integer(), String(), Integer(), String(), Integer(), _returns=Array(Mensaje))
    def transferencia_interbancaria(request, n_cuenta_o, nom_banco_o, n_cuenta_d, nom_banco_d, mon):
        cli_o1 = Cliente.objects.get(id_cuenta=n_cuenta_o)
        cli_d = Cliente.objects.get(id_cuenta=n_cuenta_d)
        if mon <= cli_o1.id_cuenta.monto:
            restante = cli_o1.id_cuenta.monto - mon
            agregacion = cli_d.id_cuenta.monto + mon
            fecha = datetime.datetime.today()
            id = cli_o1.id_cuenta
            trans = Transferencia(fecha_trans=fecha.today(), tipo_trans="Interbancaria", id_cuenta=id)
            trans.save()
            cue_o = Cuenta.objects.get(num_cuenta=cli_o1.id_cuenta.num_cuenta)
            cue_d = Cuenta.objects.get(num_cuenta=cli_d.id_cuenta.num_cuenta)
            cue_o.monto = restante
            cue_o.save()
            cue_d.monto = agregacion
            cue_d.save()

            b1 = Banco.objects.get(nombre=cli_o1.id_cuenta.id_Banco.nombre)
            id = cli_o1.id_cuenta
            cli_o = Cliente.objects.filter(id_cuenta=n_cuenta_o).values('cedula','nombres', 'username', 'password', 'id_cuenta__num_cuenta')
            cu = Cuenta.objects.filter(num_cuenta=n_cuenta_o).values('num_cuenta', 'monto')
            tran = Transferencia.objects.filter(id_cuenta=n_cuenta_o).values('fecha_trans','tipo_trans').latest("id")
            trans1 = Transferencia.objects.latest("id")
            c = list(cli_o)
            cu = list(cu)
            del c[0]['password']
            c[0]['estado'] = "Deposito Exitoso"
            c[0]['Banco'] = b1.nombre
            c[0]['num_cuenta'] = cu[0].get('num_cuenta')
            c[0]['monto'] = cu[0].get('monto')
            c[0]['id_trans'] = trans1.id
            c[0]['fecha_trans'] = tran.get('fecha_trans')
            c[0]['tipo_trans'] = tran.get('tipo_trans')
            return c
        else:
            return "Excede Monto"

    @rpc(Integer(), String(), Integer(), Integer(), _returns=Array(Mensaje))
    def transferencia_bancaria(request, n_cuenta_o, nom_banco_o, n_cuenta_d, mon):
        cli_o1 = Cliente.objects.get(id_cuenta=n_cuenta_o)
        cli_d = Cliente.objects.get(id_cuenta=n_cuenta_d)
        if cli_o1.id_cuenta.id_Banco.nombre == cli_d.id_cuenta.id_Banco.nombre:
            if mon <= cli_o1.id_cuenta.monto:
                restante = cli_o1.id_cuenta.monto - mon
                agregacion = cli_d.id_cuenta.monto + mon
                fecha = datetime.datetime.today()
                id = cli_o1.id_cuenta
                trans = Transferencia(fecha_trans=fecha.today(), tipo_trans="Bancaria", id_cuenta=id)
                trans.save()
                cue_o = Cuenta.objects.get(num_cuenta=cli_o1.id_cuenta.num_cuenta)
                cue_d = Cuenta.objects.get(num_cuenta=cli_d.id_cuenta.num_cuenta)
                cue_o.monto = restante
                cue_o.save()
                cue_d.monto = agregacion
                cue_d.save()

                b1 = Banco.objects.get(nombre=cli_o1.id_cuenta.id_Banco.nombre)
                id = cli_o1.id_cuenta
                cli_o = Cliente.objects.filter(id_cuenta=n_cuenta_o).values('cedula','nombres', 'username', 'password', 'id_cuenta__num_cuenta')
                cu = Cuenta.objects.filter(num_cuenta=n_cuenta_o).values('num_cuenta', 'monto')
                tran = Transferencia.objects.filter(id_cuenta=n_cuenta_o).values('fecha_trans','tipo_trans').latest("id")
                trans1 = Transferencia.objects.latest("id")
                c = list(cli_o)
                cu = list(cu)
                del c[0]['password']
                c[0]['estado'] = "Deposito Exitoso"
                c[0]['Banco'] = b1.nombre
                c[0]['num_cuenta'] = cu[0].get('num_cuenta')
                c[0]['monto'] = cu[0].get('monto')
                c[0]['id_trans'] = trans1.id
                c[0]['fecha_trans'] = tran.get('fecha_trans')
                c[0]['tipo_trans'] = tran.get('tipo_trans')
                return c
            else:
                print("no alcanza")
                return "Excede Monto"
        return "Error No son las mismos bancos"



    @rpc(Integer(), String(), String(), Integer(), _returns=Array(Mensaje))
    def deposito_retiro(ctx, n_cuenta_o, nom_banco_o, tipo, mon):
        cli_o1 = Cliente.objects.get(id_cuenta=n_cuenta_o)
        if tipo == "Deposito":
            agregacion = cli_o1.id_cuenta.monto + mon
            fecha = datetime.datetime.today()
            id = cli_o1.id_cuenta
            trans = Transferencia(fecha_trans=fecha.today(), tipo_trans="Deposito", id_cuenta=id)
            trans.save()
            cue_o = Cuenta.objects.get(num_cuenta=cli_o1.id_cuenta.num_cuenta)
            cue_o.monto = agregacion
            cue_o.save()

            b1 = Banco.objects.get(nombre=cli_o1.id_cuenta.id_Banco.nombre)
            id = cli_o1.id_cuenta
            cli_o = Cliente.objects.filter(id_cuenta=n_cuenta_o).values('cedula','nombres', 'username', 'password', 'id_cuenta__num_cuenta')
            cu = Cuenta.objects.filter(num_cuenta=n_cuenta_o).values('num_cuenta', 'monto')
            tran = Transferencia.objects.filter(id_cuenta=n_cuenta_o).values('fecha_trans','tipo_trans').latest("id")
            trans1 = Transferencia.objects.latest("id")
            c = list(cli_o)
            cu = list(cu)
            del c[0]['password']
            c[0]['estado'] = "Deposito Exitoso"
            c[0]['Banco'] = b1.nombre
            c[0]['num_cuenta'] = cu[0].get('num_cuenta')
            c[0]['monto'] = cu[0].get('monto')
            c[0]['id_trans'] = trans1.id
            c[0]['fecha_trans'] = tran.get('fecha_trans')
            c[0]['tipo_trans'] = tran.get('tipo_trans')
            return c
        elif tipo == "Retiro":
            if mon <= cli_o1.id_cuenta.monto:
                restante = cli_o1.id_cuenta.monto - mon
                fecha = datetime.datetime.today()
                id = cli_o1.id_cuenta
                trans = Transferencia(fecha_trans=fecha.today(), tipo_trans="Retiro", id_cuenta=id)
                trans.save()
                cue_o = Cuenta.objects.get(num_cuenta=cli_o1.id_cuenta.num_cuenta)
                cue_o.monto = restante
                cue_o.save()

                cli_o1 = Cliente.objects.get(id_cuenta=n_cuenta_o)
                b1 = Banco.objects.get(nombre=cli_o1.id_cuenta.id_Banco.nombre)
                id = cli_o1.id_cuenta
                cli_o = Cliente.objects.filter(id_cuenta=n_cuenta_o).values('cedula','nombres', 'username', 'password', 'id_cuenta__num_cuenta')
                cu = Cuenta.objects.filter(num_cuenta=n_cuenta_o).values('num_cuenta', 'monto')
                tran = Transferencia.objects.filter(id_cuenta=n_cuenta_o).values('fecha_trans','tipo_trans').latest("id")
                trans1 = Transferencia.objects.latest("id")
                c = list(cli_o)
                cu = list(cu)
                del c[0]['password']
                c[0]['estado'] = "Retiro Exitoso"
                c[0]['Banco'] = b1.nombre
                c[0]['num_cuenta'] = cu[0].get('num_cuenta')
                c[0]['monto'] = cu[0].get('monto')
                c[0]['id_trans'] = trans1.id
                c[0]['fecha_trans'] = tran.get('fecha_trans')
                c[0]['tipo_trans'] = tran.get('tipo_trans')
                return c
            else:
                return "Excede Monto"
        return "Deposito/Retiro Erroneo"
    
    



soap_app = Application(
    [SoapService],
    tns='django.soap.example',
    in_protocol = Soap11(validator='lxml'),
    out_protocol=Soap11(),
)

def consulta():
    django_soap_app = DjangoApplication(soap_app)
    my_soap_app = csrf_exempt(django_soap_app)
    return my_soap_app
