# -*- coding: utf-8 -*-
"""
Created on Thu Feb 08 13:51:36 2018

@author: alexkreamas
"""

import sqlalchemy


nHost = 'localhost'
nUser = 'root'
nPass = 'kreamas080712'
nDeBe = 'priceweb'


class dbConect:
    
    #Conexiones con MySQL
                
    @staticmethod
    def ehost():        
        
        engine = sqlalchemy.create_engine('mysql://' + nUser + ':' + nPass + '@' + nHost + '/' + nDeBe, echo = False)
        return engine
