from django.db.models import fields
from django.http.response import HttpResponse, JsonResponse
from serviciosBancarios.models import Banco, Cliente, Cuenta, Transferencia
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.forms.models import model_to_dict
import json
import datetime
# Create your views here.

@csrf_exempt
def login_page(request):
    bancos = Banco.objects.all()
    print(bancos)
    if request.method == "POST":
        print("metodo login si entra")
        username = request.POST['username']
        password = request.POST['password']
        #ban = request.POST['bancos']
        #print("USERNAME: {} - PASSWORD: {} ".format(username, password))
        cliente = Cliente.objects.get(username=username, password=password)
        #print(cliente.id_cuenta.id_Banco.nombre)
        if cliente.id_cuenta.id_Banco.nombre == request.POST['bancos']:
            if cliente:
                cuenta = Cuenta.objects.get(num_cuenta=cliente.id_cuenta.num_cuenta)
                banco = Banco.objects.get(nombre=cliente.id_cuenta.id_Banco.nombre)
                #print("AQUI :", cliente)
                request.session['cliente'] = serializers.serialize('json', [cliente, cuenta, banco])
                return render(request, "index_cliente.html", {"cliente": cliente, "cuenta": cuenta, "banco": banco})
        #if cliente:
        #request.session['cliente'] = serializers.serialize('json', [cliente, ])[0]
        
    print("metodo login no entra")
    return render(request, "login.html", {"bancos": bancos})

#@csrf_exempt
"""def ingresar(request):
    username = request.POST['username']
    password = request.POST['password']
    print(username, password)
    cliente = Cliente.validar_login(username, password)
    print("CLIENTE OE: ", cliente)
    if cliente:
        print("entro al if")
        request.session['cliente'] = serializers.serialize('json', [cliente, ])[0]
        return render(request, "index_cliente.html", {"cliente": cliente})
    else:
        print("no entro al if sino al else")
        return render(request, "login.html")"""

def obt_sesion(request):
    print(request.session['cliente'])
    bancos = Banco.objects.all()
    if "cliente" in request.session:
        result = (request.session.get("cliente"))
        d = json.loads(result)
        #print(d[1]["fields"])
    else:
        d = False
    #print(result)
    ctx = {"cliente": d[0]["fields"], "cuenta": d[1]["fields"], "banco": d[2]["fields"], "all_bancos": bancos}
    return render(request, "interbancaria.html", ctx)

def obt_datos_trans_inter(request):
    if request.method == "POST":
        bancos = Banco.objects.all()
        if "cliente" in request.session:
            result = (request.session.get("cliente"))
            d = json.loads(result)
            n_cue_o = d[1]["fields"]["num_cuenta"]
            nom_ban_o = d[2]["fields"]["nombre"]
            monto = int(request.POST['monto'])
            n_cue_d = int(request.POST['numerocuenta'])
            nom_ban_d = request.POST['ban']
            print(type(n_cue_o), type(nom_ban_o), type(n_cue_d), type(nom_ban_d), type(monto))
            urll = '/inter/{}/{}/{}/{}/{}/'.format(n_cue_o, nom_ban_o.replace(" ", ""), n_cue_d, nom_ban_d.replace(" ", ""), monto)
            return redirect(urll)
        else:
            d = False
    ctx = {"cliente": d[0]["fields"], "cuenta": d[1]["fields"], "banco": d[2]["fields"], "all_bancos": bancos}

    print("metodo login no entra")
    return render(request, "interbancaria.html", ctx)
        

def transferencia_interbancaria(request, n_cuenta_o, nom_banco_o, n_cuenta_d, nom_banco_d, mon):
    #print(n_cuenta_o, nom_banco_o, n_cuenta_d, nom_banco_d, mon)
    cli_o = Cliente.objects.get(id_cuenta=n_cuenta_o)
    cli_d = Cliente.objects.get(id_cuenta=n_cuenta_d)
    if mon <= cli_o.id_cuenta.monto:
        restante = cli_o.id_cuenta.monto - mon
        agregacion = cli_d.id_cuenta.monto + mon
        fecha = datetime.datetime.today()
        #print(restante)
        id = cli_o.id_cuenta
        trans = Transferencia(fecha_trans=fecha.today(), tipo_trans="Interbancaria", id_cuenta=id)
        trans.save()
        cue_o = Cuenta.objects.get(num_cuenta=cli_o.id_cuenta.num_cuenta)
        cue_d = Cuenta.objects.get(num_cuenta=cli_d.id_cuenta.num_cuenta)
        #print("CUENTAAAAAAAAA", type(cue_o.monto))
        cue_o.monto = restante
        cue_o.save()
        cue_d.monto = agregacion
        cue_d.save()
        trans1 = Transferencia.objects.latest("id")
        #cli_d.id_cuenta.monto = agregacion
        #cli_d.id_cuenta.monto.save()
        #print("si alcanza", type(json.dumps(trans1.id_cuenta)))
        #data = serializers.serialize('json', trans1.id_cuenta)
        return JsonResponse({"id": trans1.id, "fecha_trans": trans1.fecha_trans, "tipo_trans": trans1.tipo_trans, "cuenta": model_to_dict(trans1.id_cuenta), "cliente": model_to_dict(cli_o)})
        #print("si alcanza", trans1.id)
    else:
        print("no alcanza")
    print("CLIENTE ORIGEEN: {}".format(cli_o.nombres))
    print("CLIENTE destino: {}".format(cli_d.nombres))
    return JsonResponse({"mensaje": "TRANSFERENCIA INTERBANCARIA ERRONEA"})
    

