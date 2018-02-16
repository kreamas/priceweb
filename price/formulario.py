# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 21:56:09 2018

@author: alexkreamas
"""

from pydlm import dlm, trend, seasonality
import pandas as pd
import numpy as np
import scipy.stats


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

