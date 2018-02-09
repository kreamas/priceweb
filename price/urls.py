# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 13:42:59 2018

@author: alexkreamas
"""

from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
               
    #links
    url(r'^$', views.home, name='home'),
    url(r'^priceAnalysis/$', views.priceAnalysis, name='priceAnalysis'),    
    

    #Procedimientos (para las formas)
    url(r'pricescrap$', views.pricescrap, name='pricescrap'),
]