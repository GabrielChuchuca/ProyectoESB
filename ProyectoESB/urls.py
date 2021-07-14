"""ProyectoESB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from serviciosBancarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_page/', views.login_page),
    path('sesion/', views.obt_sesion),
    path('obtdatos/', views.obt_datos_trans_inter),
    path('inter/<int:n_cuenta_o>/<str:nom_banco_o>/<int:n_cuenta_d>/<str:nom_banco_d>/<int:mon>/', views.transferencia_interbancaria),
    path('sesion_b/', views.obt_sesion_b),
    path('obtdatos_b/', views.obt_datos_trans_banca),
    path('banca/<int:n_cuenta_o>/<str:nom_banco_o>/<int:n_cuenta_d>/<int:mon>/', views.transferencia_bancaria),



]
