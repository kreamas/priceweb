#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 11:18:40 2018

@author: alexkreamas
"""

from precioFarmacia import precioFarmacia
import pandas as pd
from formulario import formulario
from dbConect import dbConect
import datetime




#cambio = pd.read_csv("C:/KREA MAS/DATOS PARA WEB PRICE/cambio.csv")
#cambio.to_sql(name = 'catcambio', con = dbConect.ehost(), if_exists = 'replace', index = False, chunksize = 1000)
#print(cambio.head(5))


#catalogos = pd.read_csv("C:/KREA MAS/DATOS PARA WEB PRICE/catalogos.csv")
#catalogos.to_sql(name = 'catdosis', con = dbConect.ehost(), if_exists = 'replace', index = False, chunksize = 1000)
#print(catalogos.head(5))

#catalogos = pd.read_csv("C:/KREA MAS/DATOS PARA WEB PRICE/cathomologado.csv")
#catalogos.to_sql(name = 'cathomologado', con = dbConect.ehost(), if_exists = 'replace', index = False, chunksize = 1000)
#print(catalogos.head(5))


#farmacia = pd.read_csv("C:/KREA MAS/DATOS PARA WEB PRICE/FARMACIAS SAN PABLO.csv", sep = "|")
#farmacia.drop(farmacia.columns[[0]], axis=1, inplace=True)
#farmacia.to_sql(name = 'precios', con = dbConect.ehost(), if_exists = 'replace', index = False, chunksize = 1000)
#print(farmacia.head(5))
#print(list(farmacia))

#Nos quedamos solo con los que están en el catalogo
catDF = pd.read_sql('select * from cathomologado', con = dbConect.ehost())

#Nos quedamos con los diferentes de NULL
catDF = catDF[catDF['SKU'].notnull()]
              
#Concatenamos Fuente - SKU
catDF['cadena'] = catDF['FUENTE'] + '@' + catDF['SKU']

#Borramos Fuente y SKU (solo nos interesan los homologados)
catDF = catDF.drop(['FUENTE'], axis = 1)
catDF = catDF.drop(['SKU'], axis = 1)


#Nos quedamos solo con los que están en el catalogo
catDosis = pd.read_sql('select * from catdosis', con = dbConect.ehost())



#farmacia = [['COMERCIAL MEXICANA','http://www.superensucasa.com/ccm/goBusqueda.action?succId=329&ver=mislistas&succFmt=100#/'],['HEB', 'http://www.heb.com.mx/catalogsearch/result/index/?cat=+995+&limit=36&q='], ['FARMACIAS SAN PABLO', 'https://www.farmaciasanpablo.com.mx/search/?text='], ['FARMACIAS DEL AHORRO', 'http://www.fahorro.com/catalogsearch/result/?q=']]
#farmacia = [['CHEDRAUI', 'https://www.chedraui.com.mx/chedrauistorefront/chedraui/es/search/?text='], ['SANBORNS', 'http://buscador.sanborns.com.mx/search?client=Sanborns&output=xml_no_dtd&proxystylesheet=Sanborns&sort=date:D:L:d1&oe=UTF-8&ie=UTF-8&ud=1&exclude_apps=1&site=Sanborns&ulang=es&access=p&entqr=3&entqrm=0&filter=0&getfields=*&q='], ['FARMALISTO', 'https://www.farmalisto.com.mx/buscar?controller=search&orderby=position&orderway=desc&search_query='],['FARMACIAS GI', 'http://farmaciasgi.com.mx/?s='], ['WALMART', 'https://super.walmart.com.mx/search/?_dyncharset=UTF-8&_dynSessConf=-833724501808047001&Dy=1&Nty=1&typSub=1&Ntt='], ['FARMATODO', 'https://www.farmatodo.com.mx/buscar/Buscar/1/?q='], ['FARMASMART', 'https://farmasmart.com/buscar?controller=search&orderby=position&orderway=desc&search_query='], ['HEB', 'http://www.heb.com.mx/catalogsearch/result/index/?cat=+995+&limit=36&q='], ['FARMACIAS SAN PABLO', 'https://www.farmaciasanpablo.com.mx/search/?text='], ['FARMACIAS DEL AHORRO', 'http://www.fahorro.com/catalogsearch/result/?q=']]
#farmacia = [['FARMASMART', 'https://farmasmart.com/buscar?controller=search&orderby=position&orderway=desc&search_query=']]
#prodz = ['MICARDIS', 'TRAYENTA', 'JARDIAN', 'ATACAND', 'DIOVAN', 'SPIRIVA']
prodz = ['RIVOTRIL', 'KEPPRA', 'LYRICA', 'ATEMPERATOR', 'KRIADEX', 'ANTIFLU', 'SENSIBIT', 'XL-3', 'XL3', 'DESENFRIOL', 'MICARDIS', 'ATACAND', 'DIOVAN', 'BICARTIAL', 'ACTRON', 'RANTUDIL', 'MOBICOX', 'NEXIUM', 'ULSEN', 'INHIBITRON', 'TECTA', 'JANUMET', 'JANUVIA', 'TRAYENTA', 'JARDIANZ', 'PRE-DIAL', 'PREDIAL', 'TEMPRA', 'ASPIRINA', 'MELUBRINA', 'SEDALMERCK', 'MOTRIN', 'NAN', 'ENFAGROW', 'PROGRESS', 'ENTEROGERMINA', 'SINUBERASE', 'IPRIKENE']
#prodz = ['NAN', 'ENFAGROW']

#tienda = ['FARMACIAS SAN PABLO', 'FARMACIAS DEL AHORRO', 'HEB', 'FARMASMART', 'FARMATODO', 'WALMART', 'FARMACIAS GI', 'FARMALISTO', 'SANBORNS', 'CHEDRAUI']
#tienda = ['FARMACIAS SAN PABLO', 'FARMACIAS DEL AHORRO', 'HEB', 'FARMASMART', 'FARMATODO', 'WALMART', 'FARMALISTO', 'SANBORNS', 'CHEDRAUI']
tienda = ['FARMACIAS SAN PABLO', 'FARMACIAS DEL AHORRO', 'HEB', 'FARMASMART', 'FARMATODO', 'WALMART', 'FARMALISTO', 'CHEDRAUI']
#tienda = ['FARMACIAS DEL AHORRO']
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


            
#Reemplazamos en la lista los espacios en blanco

producto = []
for prod in prodz:
    prod = prod.replace(" ", "+")
    producto.append(prod)



fecha = datetime.datetime.now().date()
pais = "MEXICO"
cliente = "GENERAL"


#for i in range(1):
for i in range(len(farmacia)):
    datos = []
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

    for j in range(len(prize)):
        prize[j].append(farma)        
        prize[j].append(fecha)
        datos.append(prize[j])

    if i == 0:
        dfPrice = pd.DataFrame(datos)
        dfPrice.columns = ['Sku', 'Precio', 'Farmacia', 'Fecha']  
    else:
        ndf = pd.DataFrame(datos)
        ndf.columns = ['Sku', 'Precio', 'Farmacia', 'Fecha']
        dfPrice = pd.concat([dfPrice, ndf])
        

#Concatenamos Farmacia - Sku
dfPrice['cadena'] = dfPrice['Farmacia'] + '@' + dfPrice['Sku']

rDF = dfPrice.merge(catDF, on = 'cadena', how = 'left')
rDF = rDF.drop(['cadena'], axis = 1)
rDF = rDF.drop(['Sku'], axis = 1)
rDF = rDF[rDF['HOMOLOGADO'].notnull()]
rDF['pais'] = pais
rDF['cliente'] = cliente

print(rDF)

          
#Unimos con el catalogo de dosis
oDF = rDF.merge(catDosis, on='HOMOLOGADO', how = 'left')
oDF['ppack'] = oDF['Precio'] / oDF['PACK']
oDF['dots'] = oDF['ppack'] * oDF['DOSIS']
print(oDF)



oDF = oDF[['pais', 'cliente', 'Farmacia', 'MERCADO', 'GENERO', 'FFARMA_1', 'FFARMA_2', 'LABORATORIO', 'FAMILIA', 'MARCA', 'HOMOLOGADO', 'Precio', 'PACK', 'DOSIS', 'INDICE', 'COMPLIANCE', 'ppack', 'dots']]
oDF['fecha'] = fecha

del rDF
del catDosis

print(oDF.head(10))        
oDF.to_csv('C:/KREA MAS/DATOS PARA WEB PRICE/FARMACIAS.csv', sep='|')
oDF.to_sql(name = 'precios', con = dbConect.ehost(), if_exists = 'append', index = False, chunksize = 1000)

del dfPrice
del catDF



#dfPrice.to_sql(name = 'precios', con = dbConect.ehost(), if_exists = 'append', index = False, chunksize = 1000)

 #lineasDF = pd.read_sql('select * from lineas', con = formulario.ehost())


print('ya termine')
#dfPrice.to_csv('C:/KREA MAS/DATOS PARA WEB PRICE/precios.csv', sep='|')
#print(dfPrice)