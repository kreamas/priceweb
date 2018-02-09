# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 13:07:55 2018

@author: alexkreamas
"""

from urllib import urlopen
from bs4 import BeautifulSoup
import numpy as np
from formulario import formulario

class precioFarmacia:
    
    

    #Este es para Chedraui
    @staticmethod
    def farmaciaChedraui(lista, farmacia, sitio, tienda):
        
        print(farmacia)
        
        producto = lista
        
        lizta = []
        
        for prod in producto:
            busca=urlopen(sitio + prod)
            bsObj=BeautifulSoup(busca.read(), "lxml")
            nombres = bsObj.findAll("a", {"class": "product__list--name"})
            precios = bsObj.findAll("div", {"class": "product__listing--price price-colour-final"})
            
            for i in range(len(nombres)):
                nombre = formulario.reemplazaAzento(nombres[i].text.strip().encode('utf-8'))
                precio = precios[np.int(i)*np.int(2)].text.strip()[1:]
                precio = precio.replace(",","")
                precio = precio.replace("$","")
                
                lizta.append([np.str(nombre), np.float(precio)])                            
                print(nombre + ": " + precio)
        
        return lizta

    
    
    #Este es para Sanborns
    @staticmethod
    def farmaciaSanborns(lista, farmacia, sitio, tienda):
        
        producto = lista
        
        print(farmacia)

        lizta = []
        
        for prod in producto:
            busca=urlopen(sitio + prod)
            bsObj=BeautifulSoup(busca.read(), "lxml")
            nombres = bsObj.findAll("span", {"class": "Pay_pal"})
            precios = bsObj.findAll("span", {"class": "Pay_pal1"})
            
            for i in range(len(nombres)):
                try:
                    nombre = formulario.reemplazaAzento(nombres[i].text.strip().encode('utf8'))
                    precio = precios[i].text.strip()[1:]                
                    precio = precio.replace(",","")
                    precio = precio.replace("$","")
    
                    lizta.append([np.str(nombre), np.float(precio)])                            
                    print(nombre + ": " + precio)
                except:
                    pass
        return lizta


    #Este es para Farmalisto
    #Aquí hay algo interesante ya que ponen productos que suelen ver o comprar juntos
    @staticmethod
    def farmaciaListo(lista, farmacia, sitio, tienda):
        
        producto = lista
        
        print(farmacia)
        
        lizta = []
        
        for prod in producto:
            busca=urlopen(sitio + prod + '&submit_search=Buscar')
            bsObj=BeautifulSoup(busca.read(), "lxml")
            nombres = bsObj.findAll("div", {"class": "name_product_search"})
            precios = bsObj.findAll("div", {"class": "content_price"})
            
            for i in range(len(nombres)):
                try:
                    nombre = formulario.reemplazaAzento(nombres[i].text.strip().encode('utf8'))
                    precio = precios[i].text.strip()[2:]                
                    precio = precio.replace(",","")
                    precio = precio.replace("$","")
    
                    lizta.append([np.str(nombre), np.float(precio)])                            
                    print(nombre + ": " + precio)
                except:
                   pass 
        return lizta


    #Este es para Farmacias GI
    @staticmethod
    def farmaciaGI(lista, farmacia, sitio, tienda):
        
        producto = lista
        
        print(farmacia)
        
        lizta= []
        
        for prod in producto:
            busca=urlopen(sitio + prod + '&post_type=product')
            bsObj=BeautifulSoup(busca.read(), "lxml")
            infos = bsObj.findAll("div", {"class": "prodDescCorta"})
            
            for info in infos:
                precio = info.find("span", {"class":"amount"}).text.strip()                
                nombre = formulario.reemplazaAzento(info.text.strip()[:-(len(precio)+8)].encode('utf8'))

                precio = precio.replace(",","")
                precio = precio.replace("$","")

                lizta.append([np.str(nombre), np.float(precio)])                            

                print(nombre + ": " + precio)
        return lizta    


    
    #Este es para Walmart
    @staticmethod
    def farmaciaWalmart(lista, farmacia, sitio, tienda):
        
        producto = lista
        
        print(farmacia)

        lizta = []        
        
        for prod in producto:
            busca=urlopen(sitio + prod)
            bsObj=BeautifulSoup(busca.read(), "lxml")
            nombres = bsObj.findAll("div", {"class": "product-title"})
            precios = bsObj.findAll("div", {"class": "price-wrap p-price price"})
            
            for i in xrange(0, len(precios)):
                try:
                    nombre = formulario.reemplazaAzento(nombres[i].find("span", {"itemprop": "name"}).text.strip().encode('utf8'))
                    precio = precios[i].find("span", {"itemprop":"price"}).text           
                    precio = precio.replace(",","")
                    precio = precio.replace("$","")
    
                    lizta.append([np.str(nombre), np.float(precio)])                            

                    print(nombre + ": " + precio)
                except:
                    pass
        return lizta
    
    
    
    #Este es para Farmatodo
    @staticmethod
    def farmaciaFarmaTodo(lista, farmacia, sitio, tienda):
        
        producto = lista
        
        print(farmacia)
        
        lizta = []
        
        for prod in producto:
            busca=urlopen(sitio + prod)
            bsObj=BeautifulSoup(busca.read(), "lxml")
            nombres = bsObj.findAll("div", {"class": "col-md-6"})
            precios = bsObj.findAll("div", {"class": "col-md-4"})
            
            for i in xrange(1, len(nombres)-4):
                try:
                    nombre = formulario.reemplazaAzento(nombres[i].find("a").text.strip().encode('utf8'))
                    precio = precios[i].find("p").text.strip()[9:].strip()[1:]            
                    precio = precio.replace(",","")
                    precio = precio.replace("$","")
    
                    lizta.append([np.str(nombre), np.float(precio)])                            
    
                    print(nombre + ": " + precio)
                except:
                    pass
        return lizta
    
    
    #Este es para FarmaSmart
    @staticmethod
    def farmaciaFarmaSmart(lista, farmacia, sitio, tienda):
        
        producto = lista
        
        print(farmacia)
        
        lizta = []
        
        for prod in producto:
            busca=urlopen(sitio + prod)
            bsObj=BeautifulSoup(busca.read(), "lxml")
            info = bsObj.findAll("div", {"class":"product-container"})
            
            for infos in info:
                nombres = formulario.reemplazaAzento(infos.find("a", {"class": "product_img_link"}).attrs['title'].encode('utf8'))
                precios = infos.find("span", {"class":"price product-price"}).text[2:]            
                precios = precios.replace(",","")
                precios = precios.replace("$","")

                lizta.append([np.str(nombres), np.float(precios)])                            

                print(nombres + ": " + precios)
        return lizta
                
        

    
    #Este es para Farmacias del Ahorro
    @staticmethod
    def farmaciaDelAhorro(lista, farmacia, sitio, tienda):
        
        producto = lista
        
        print(farmacia)
        
        lizta = []
        
        for prod in producto:
            busca=urlopen(sitio + prod)
            bsObj=BeautifulSoup(busca.read(), "lxml")
            links = bsObj.findAll("h2")
            
            for link in links:
                try:
                    vinculo = link.find("a").attrs['href']
                    html = urlopen(vinculo)
                    vusca = BeautifulSoup(html.read(), "lxml")
                    precio = vusca.findAll("span", {"class": "price"})[0].text
                    nombre = formulario.reemplazaAzento(vusca.find("title").text.strip().encode('utf8'))

                    precio = precio.replace(",","")
                    precio = precio.replace("$","")
    
                    lizta.append([np.str(nombre), np.float(precio)])                            
                    
                    print(nombre + ": " + precio)
                except:
                    pass
        return lizta
            

    @staticmethod
    def farmaciaHEB(lista, farmacia, sitio, tienda):
        
        producto = lista
        print(farmacia)
        
        lizta = []
        
        for prod in producto:
            busca=urlopen(sitio + prod)
            bsObj=BeautifulSoup(busca.read(), "lxml")
            info = bsObj.findAll("div", {"class":"product-info"})
            
            for infos in info:
                nombres = formulario.reemplazaAzento(infos.find("h2", {"class":"product-name"}).find("a").attrs['title'].strip().encode('utf8'))
                precios = infos.find("span", {"class":"price"}).text[2:].strip()            
                precios = precios.replace(",","")
                precios = precios.replace("$","")

                lizta.append([np.str(nombres), np.float(precios)])  
                try:                          
                    print(nombres + ": " + precios)
                except:
                    pass

        return lizta
                
        
        
    #Este es para Farmacias San Pablo
    @staticmethod    
    def farmaciaSanPablo(lista, farmacia, sitio, tienda):
        
        producto = lista
        print(farmacia)
        
        lizta = []
        
        for prod in producto:
            busca=urlopen(sitio + prod)
            bsObj=BeautifulSoup(busca.read(), "lxml")
            nombres = bsObj.findAll("p", {"class": "item-title"})
            subnombres = bsObj.findAll("p", {"class": "item-subtitle"})
            precios = bsObj.findAll("p", {"class": "item-prize"})
            
            for i in range(len(nombres)):
                nombre = formulario.reemplazaAzento(nombres[i].text.strip().encode('utf8'))
                #nombre = nombres[i].text.strip()
                
                subnombre = formulario.reemplazaAzento(subnombres[i].text.strip().encode('utf8'))
                precio = precios[i].text.strip()[:-4]

                precio = precio.replace(",","")
                precio = precio.replace("$","")

                lizta.append([np.str(nombre) + " ( " + np.str(subnombre) + ")", np.float(precio)])                            
                #lizta.append([nombre, np.float(precio)])                            

                
                print(nombre + " (" + subnombre + "): " + precio)
        return lizta
        