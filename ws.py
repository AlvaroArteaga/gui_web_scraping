import os
from descarga_ifc import *

#ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).rsplit(os.sep, 1)[0]+"\ifc"
#ruta=str(ROOT_DIR)

#Procesos =['BADX', 'BAEN', 'EFAC','FETR','PJDX','PMGD','RCUT']

#for  proceso in Procesos:
#    for mes in range(1,13):
#        descarga(proceso,mes,2022,ruta)

def ws_aa(procesos,mesi,anoi,mesf,anof,modo,ruta):
    print("TEST: ",ruta)
    if modo:
        for  proceso in procesos:
            if anoi != anof:
                for anno in range(int(anoi),int(anof)-int(anoi)+1):
                    if anno == int(anof): mes_fn=mesf
                    else: mes_fn=12
                    if anno == int(anoi): mes_in=mesi
                    else: mes_fn=1
                    for mes in range(mes_in,mes_fn+1):
                        descarga(proceso,mes,anno,ruta)
            else:
                for mes in range(mesi,mesf+1):
                        print("-----------------++++++++++--",mes)
                        descarga(proceso,mes,anoi,ruta)
    else:
        for  proceso in procesos:
            descarga(proceso,mesi,anoi,ruta)
