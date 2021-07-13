from serviciosBancarios.models import Banco, Cliente
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

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
        print("USERNAME: {} - PASSWORD: {} ".format(username, password))
        cliente = Cliente.objects.get(username=username, password=password)
        print(cliente.id_cuenta.id_Banco.nombre)
        if cliente.id_cuenta.id_Banco.nombre == request.POST['bancos']:
            if cliente:
                print("AQUI :", cliente)
                return render(request, "index_cliente.html", {"cliente": cliente})
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

def cuenta(request):
    print(request.session['cliente'])
    if "cliente" in request.session:
        result = request.session.get("cliente")
    else:
        result = False
    print(result)
    ctx = {"cliente": result}
    return render(request, "account.html", ctx)
