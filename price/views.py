# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required


import pandas as pd
import numpy as np
import csv
from formulario import formulario
from precioFarmacia import precioFarmacia

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.interactive as r

importr(str("forecast"))



import json


# Create your views here.

#Links
@login_required
def home(request):
    return render(request, 'price/priceAnalysis.html')

@login_required
def priceAnalysis(request):
    return render(request, 'price/priceAnalysis.html')



        
#Procedimientos        

def pricescrap(request):

    #data = [['saludo', 'dato'], ['hola', 1], ['adios', 2], ['bye', 3]]
    #return JsonResponse({'precizo': data})
    
    tienda = request.GET.getlist('tienda')  #diccionario, lo que viene dentro del parentesis es el nombre del input text de html, al ser un diccionario podemos usar su metodo get
    productos = request.GET.get('productos')  #diccionario, lo que viene dentro del parentesis es el nombre del input text de html, al ser un diccionario podemos usar su metodo get
    prodCliente = request.GET.getlist('prod_cliente')  #diccionario, lo que viene dentro del parentesis es el nombre del input text de html, al ser un diccionario podemos usar su metodo get


    productos = productos.split(",")
    productos = [producto.strip() for producto in productos]

                 
    farmaciaz = [['CHEDRAUI', 'https://www.chedraui.com.mx/chedrauistorefront/chedraui/es/search/?text='], ['SANBORNS', 'http://buscador.sanborns.com.mx/search?client=Sanborns&output=xml_no_dtd&proxystylesheet=Sanborns&sort=date:D:L:d1&oe=UTF-8&ie=UTF-8&ud=1&exclude_apps=1&site=Sanborns&ulang=es&access=p&entqr=3&entqrm=0&filter=0&getfields=*&q='], ['FARMALISTO', 'https://www.farmalisto.com.mx/buscar?controller=search&orderby=position&orderway=desc&search_query='],['FARMACIAS GI', 'http://farmaciasgi.com.mx/?s='], ['WALMART', 'https://super.walmart.com.mx/search/?_dyncharset=UTF-8&_dynSessConf=-833724501808047001&Dy=1&Nty=1&typSub=1&Ntt='], ['FARMATODO', 'https://www.farmatodo.com.mx/buscar/Buscar/1/?q='], ['FARMASMART', 'https://farmasmart.com/buscar?controller=search&orderby=position&orderway=desc&search_query='], ['HEB', 'http://www.heb.com.mx/catalogsearch/result/index/?cat=+995+&limit=36&q='], ['FARMACIAS SAN PABLO', 'https://www.farmaciasanpablo.com.mx/search/?text='], ['FARMACIAS DEL AHORRO', 'http://www.fahorro.com/catalogsearch/result/?q=']]

    farmacia = []
    for y in range(len(tienda)):
        tyenda = tienda[y]
        x = 0
        for j in range(len(farmaciaz)):
            if tyenda == farmaciaz[j][0]:
                farmacia.append(farmaciaz[x])
                pass
            else:
                x = x+1

    print(x)
    print(farmacia)

    #prodz = ['MICARDIS', 'TRAYENTA', 'JARDIAN', 'ATACAND', 'DIOVAN', 'SPIRIVA']
    prodz = prodCliente
    
    
    #Reemplazamos en la lista los espacios en blanco
    
    producto = []
    for prod in prodz:
        prod = prod.replace(" ", "+")
        producto.append(prod)
    
    
    datos = []
    
    #for i in range(1):
    for i in range(len(farmacia)):
        datoz = [['Sku', 'Precio']]
        print('')
        farma = farmacia[i][0]
        if farma == "FARMACIAS SAN PABLO":
            prize = precioFarmacia.farmaciaSanPablo(producto, farmacia[i][0], farmacia[i][1], farma)
        elif farma == "FARMACIAS DEL AHORRO":
            prize = precioFarmacia.farmaciaDelAhorro(producto, farmacia[i][0], farmacia[i][1], farma)
        elif farma == "HEB":
            prize = precioFarmacia.farmaciaHEB(producto, farmacia[i][0], farmacia[i][1], farma)
        elif farma == "FARMASMART":
            prize = precioFarmacia.farmaciaFarmaSmart(producto, farmacia[i][0], farmacia[i][1], farma)
        elif farma == "FARMATODO":
            prize = precioFarmacia.farmaciaFarmaTodo(producto, farmacia[i][0], farmacia[i][1], farma)
        elif farma == "WALMART":
            prize = precioFarmacia.farmaciaWalmart(producto, farmacia[i][0], farmacia[i][1], farma)        
        elif farma == "FARMACIAS GI":
            prize = precioFarmacia.farmaciaGI(producto, farmacia[i][0], farmacia[i][1], farma)        
        elif farma == "FARMALISTO":
            prize = precioFarmacia.farmaciaListo(producto, farmacia[i][0], farmacia[i][1], farma)        
        elif farma == "SANBORNS":
            prize = precioFarmacia.farmaciaSanborns(producto, farmacia[i][0], farmacia[i][1], farma)        
        elif farma == "CHEDRAUI":
            prize = precioFarmacia.farmaciaChedraui(producto, farmacia[i][0], farmacia[i][1], farma)        
    
        for i in range(len(prize)):
            datoz.append(prize[i])
        
        datos.append(datoz)
        
    print(datos)
    
    return JsonResponse({'precizo': datos, 'tienda': tienda})
        
        

  