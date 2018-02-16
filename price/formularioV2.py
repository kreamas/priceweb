# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 21:56:09 2018

@author: alexkreamas
"""

from pydlm import dlm, trend, seasonality
import pandas as pd
import numpy as np
import scipy.stats

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import rpy2.interactive as r




class formulario:

    @staticmethod
    def reemplazaAzento(x):
        
        
        x = x.replace('Á', 'A')
        x = x.replace('á', 'a')
        x = x.replace('Â', '')        
        x = x.replace('É', 'E')
        x = x.replace('é', 'e')
        x = x.replace('È', 'E')
        x = x.replace('è', 'e')
        x = x.replace('Í', 'I')
        x = x.replace('Ì', 'I')
        x = x.replace('í', 'i')
        x = x.replace('Ó', 'O')
        x = x.replace('ó', 'o')
        x = x.replace('Ú', 'U')
        x = x.replace('ú', 'u')
        x = x.replace('Ü', 'U')
        x = x.replace('ü', 'u')
        x = x.replace('Ñ', 'N')
        x = x.replace('ñ', 'n')
        x = x.replace('+', '_')
        x = x.replace('-', '_')
        x = x.replace(',', ' ')
        x = x.replace('®', '')

        x = x.replace('\xc2', '')   
        x = x.replace('\xc3', '')
        x = x.replace('\x82', '')
        
        return x

        
    @staticmethod    
    def forecazt(datos, predice, zeazon):
        qq = scipy.stats.norm.ppf(0.5 * (1+0.95))

        lysta = ""
        for i in range(len(datos)):
            lysta = lysta + ", " + str(datos[i])
        
            
        lysta = lysta[2:]
        lysta = "c(" + lysta + ")"

            
        ro.r('datin <- ' + lysta)
        ro.r("tdatin <- ts(datin, start = c(2012,1), frequency = " + str(zeazon) + ")")
        datos = ro.r("tdatin <- tsclean(tdatin)")
        
        #Esta es la tendencia
        n1 = datos
        m1 = dlm(n1) + trend(1, discount = 1, name = 'a') + seasonality(zeazon, discount = 1, name = 'b')
        m1.fit()

        
        cons = list(n1)
        opti = list(n1)
        pesi = list(n1)
        
        
        for i in range(predice):
            if i == 0:
                (p1Mean, p1Var) = m1.predict(date = m1.n-1)        
            else:
                (p1Mean, p1Var) = m1.continuePredict()
        
            mean1 = str(p1Mean[[0]])[3:]
            mean2 = np.float(mean1[:-2])
            
            cons.append(mean2)
        
            vari1 = str(np.sqrt(p1Var[[0]]))[3:]
            vari2 = np.float(vari1[:-2])
            
            opti.append(mean2 + qq * vari2)
            pesi.append(mean2 - qq * vari2)
        
        
            
        df = pd.DataFrame()
        df['optimista'] = opti
        df['conservador'] = cons
        df['pesimista'] = pesi
        
        return df