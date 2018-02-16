
import pandas as pd
from dbConect import dbConect
import datetime




cathomologado = pd.read_csv("C:/KREA MAS/DATOS PARA WEB PRICE/cathomologado.csv", encoding='latin1')
cathomologado.to_sql(name = 'cathomologado', con = dbConect.ehost(), if_exists = 'replace', index = False, chunksize = 1000)


base = pd.read_csv("C:/KREA MAS/DATOS PARA WEB PRICE/precios.csv", sep="|")
base.to_sql(name = 'precios', con = dbConect.ehost(), if_exists = 'replace', index = False, chunksize = 1000)


cambio = pd.read_csv("C:/KREA MAS/DATOS PARA WEB PRICE/cambio.csv")
cambio.to_sql(name = 'catcambio', con = dbConect.ehost(), if_exists = 'replace', index = False, chunksize = 1000)


catalogos = pd.read_csv("C:/KREA MAS/DATOS PARA WEB PRICE/catalogos.csv")
catalogos.to_sql(name = 'catdosis', con = dbConect.ehost(), if_exists = 'replace', index = False, chunksize = 1000)


