#!/usr/bin/python2.7
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
from dbConect import dbConect
import datetime

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.interactive as r

importr(str("forecast"))

#Aqui un pequeño comentario

import json


print('adios son gokku')

# Create your views here.

#Links
@login_required
def home(request):
    return render(request, 'price/priceAnalysis.html')

@login_required
def priceAnalysis(request):
    return render(request, 'price/priceAnalysis.html')



        
#Procedimientos -------------------------------------------------------------------------------------------------        

#Para refrescar las listas

def refreshTienda(request):

    df = pd.read_sql('select * from catdosis', con = dbConect.ehost())
    mercados = sorted(list(set(df['MERCADO'].tolist())))
    #mercados = list(set(df[df['Farmacia'].isin(tienda)].tolist()))    
    
    return JsonResponse({'mercados': mercados})
    

def refreshMercado(request):
    
    mercados = request.GET.getlist('mercado')
    
    if mercados[0] == "ALL" or len(mercados) == 0:
        familias = ['ALL']
    else:    
        df = pd.read_sql('select * from catdosis', con = dbConect.ehost())    
        mercadosDF = df[df['MERCADO'].isin(mercados)]                        
        familias = sorted(list(set(mercadosDF['FAMILIA'].tolist())))    
        
    return JsonResponse({'familias': familias})
    
def refreshFamilias(request):

    mercados = request.GET.getlist('mercado')
    familias = request.GET.getlist('familia')
    
    if mercados[0] == "ALL" or familias[0] == "ALL" or len(mercados) == 0 or len(familias) == 0:
        marcas = ['ALL']
    else:    
        df = pd.read_sql('select * from catdosis', con = dbConect.ehost())    
        familiasDF = df[df['MERCADO'].isin(mercados) & df['FAMILIA'].isin(familias)]      
                      
        marcas = sorted(list(set(familiasDF['MARCA'].tolist())))    
        
    return JsonResponse({'marcas': marcas})
    

def refreshBrands(request):

    mercados = request.GET.getlist('mercado')
    familias = request.GET.getlist('familia')
    marcas = request.GET.getlist('brands')
    
    if mercados[0] == "ALL" or familias[0] == "ALL" or marcas[0] == "ALL" or len(mercados) == 0 or len(familias) == 0 or len(marcas) == 0:
        sku = ['ALL']
    else:    
        df = pd.read_sql('select * from catdosis', con = dbConect.ehost())    
        marcasDF = df[df['MERCADO'].isin(mercados) & df['FAMILIA'].isin(familias) & df['MARCA'].isin(marcas)]      
                      
        sku = sorted(list(set(marcasDF['HOMOLOGADO'].tolist())))    
        
    return JsonResponse({'sku': sku})

    

def consultaPrecios(request):
    fechaIni = request.GET.get('initial-date')
    fechaFin = request.GET.get('last-date')
    tipoChart = request.GET.get('chart-style')
    tipoMedida = request.GET.get('measure')
    tipoItem = request.GET.get('nom-item')
    verChart = request.GET.get('chart-views')
    
    
    tienda = request.GET.getlist('tienda')
    mercado = request.GET.getlist('mercado')
    familia = request.GET.getlist('familia')
    marcas = request.GET.getlist('brands')
    sku = request.GET.getlist('sku')
    
    df = pd.read_sql('select * from precios', con = dbConect.ehost())    
    df['fecha'] = pd.to_datetime(df['fecha'])    
    df['fecha'] = df['fecha'].apply(lambda x: x.date())                        
    
    

    # Filtro fechas inicial y final    
    if fechaIni == "" or fechaFin == "":
        f1 = df.copy()
    else:

        lfechaIni = fechaIni.split("-")    
        dfechaIni = datetime.date(int(lfechaIni[0]), int(lfechaIni[1]), int(lfechaIni[2]))
        
        lfechaFin = fechaFin.split("-")    
        dfechaFin = datetime.date(int(lfechaFin[0]), int(lfechaFin[1]), int(lfechaFin[2]))
        
        
        #fecha = [dfechaIni, dfechaFin]
        f1 = df[(df['fecha'] >= dfechaIni) & (df['fecha'] <= dfechaFin)]
        #f1 = df[df['fecha'].isin(fecha)]   


                
    # Filtro tienda    
    if len(tienda) == 0:
        f2 = f1.copy()
    else:
        f2 = f1[f1['Farmacia'].isin(tienda)]

    del f1
    
    #Filtro mercado
    if len(mercado) == 0 or mercado[0] == "ALL":
        f3 = f2.copy()         
    else:
        f3 = f2[f2['MERCADO'].isin(mercado)]
    
    del f2
    
    
    #Filtro familias
    if len(familia) == 0 or familia[0] == "ALL":
        f4 = f3.copy()         
    else:
        f4 = f3[f3['FAMILIA'].isin(familia)]
    
    del f3

    
    #Filtro marcas
    if len(marcas) == 0 or marcas[0] == "ALL":
        f5 = f4.copy()         
    else:
        f5 = f4[f4['MARCA'].isin(marcas)]
    
    del f4
    

    #Filtro sku
    if len(sku) == 0 or sku[0] == "ALL":
        f6 = f5.copy()         
    else:
        f6 = f5[f5['HOMOLOGADO'].isin(sku)]
    
    del f5

    #Hacemos las tablas pivote 
    
    if tipoItem == "MARKET":
        variable = "MERCADO"
    elif tipoItem == "LABORATORY":
        variable = "LABORATORIO"
    elif tipoItem == "FAMILY":
        variable = "FAMILIA"
    elif tipoItem == "BRAND":
        variable = "MARCA"
    elif tipoItem == "SKU":
        variable = "HOMOLOGADO"

    if verChart == "ITEM - STORE":
        take = [variable, 'Farmacia']
    else:
        take = ['Farmacia', variable]
        

    if tipoMedida == "LOCAL PRICE":
        medidas = 'Precio'
    elif tipoMedida == "SINGLE DOSES":
        medidas = "ppack"
    elif tipoMedida == "DOT":
        medidas = "dots"
        
        
    matriz = []

    tablon = pd.pivot_table(f6, index = take, columns = 'fecha', values = medidas, aggfunc=np.mean, dropna = True, fill_value = 0, margins = True)   
    tablon = tablon.reset_index()
    tablon = tablon.iloc[:, :-1] 
    tablon = tablon[:-1]     
    tablon = tablon.round(2)
    
    ncolumna = list(tablon)
    lista = list(set(tablon[ncolumna[0]].tolist()))

    for i in range(len(lista)):
        # Hacemos filtro para cada elemento de la lista
        tabla = tablon[tablon[ncolumna[0]].isin([lista[i]])] 
        
        l1 = list(tabla)                       
        t1  = pd.DataFrame()
        
        for x in xrange(1, len(l1)):
            t1[l1[x]] = tabla[l1[x]]


        #Cambiamos las fechas a cadenas
        
        columns = list(t1)
        
        
        for j in xrange(1, len(columns)):
            deits = unicode(columns[j])
            columns[j] = deits
        
        t1 = t1.set_index(take[1])
        t1 = t1.transpose()
        
        columns = list(t1)
        columns.insert(0, 'Date')

        rows = [[i for i in row] for row in t1.itertuples()]
        rows.insert(0, columns)
    
        matriz.append(rows)
    
        
    return JsonResponse({'matriz': matriz, 'elementos': lista, 'tchart': tipoChart})

    
    
    
    
    
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
        
        

  