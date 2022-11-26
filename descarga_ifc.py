from cgitb import text
from lib2to3.pgen2.driver import Driver
from pathlib import Path
from re import X
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

import os
import sys 


switch_mes = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}

def descarga(proceso_ejemplo, mes_ejemplo, ano_ejemplo, ruta):
    
    mes_ejemplo=switch_mes[mes_ejemplo]
    ano_ejemplo=str(ano_ejemplo)
    print("TEST: ",ruta)

    options = webdriver.ChromeOptions()
    print("1")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    print("2")
    prefs = {"download.default_directory" : ruta}
    print("3")
    options.add_experimental_option("prefs",prefs)
    print("4")
    service = Service('E:/GitHub/Coordinador_Electrico/2022/DBCD/gui_web_scraping/webdriver/chromedriver.exe')
    print("5")
    driver = webdriver.Chrome(service=service, options=options)
    print("6")

    
    driver.get('https://web.ifc.coordinador.cl/')
    print("7")
    time.sleep(1)

    driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/app-filtros-despliegue-publico/div[1]/mat-form-field[1]/div/div[1]/div').click()


    proceso=[]

  
    time.sleep(1)
    for i in range(1, 8):
        proceso.append(driver.find_element(By.XPATH,'//*[@id="cdk-overlay-0"]/div/mat-option[' + str(i) + ']').text)


    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="cdk-overlay-0"]/div/mat-option[' + str(proceso.index(proceso_ejemplo)+1) + ']').click()


    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/app-filtros-despliegue-publico/div[1]/mat-form-field[2]/div/div[1]/div').click()



    time.sleep(2)

    ano=[]
    for j in range(1, 5):
        ano.append(driver.find_element(By.XPATH,'//*[@id="cdk-overlay-1"]/div/mat-option[' + str(j) + ']').text)


    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="cdk-overlay-1"]/div/mat-option[' + str(ano.index(ano_ejemplo)+1) + ']').click()

    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/app-filtros-despliegue-publico/div[1]/mat-form-field[3]/div/div[1]/div').click()
    mes=[]
    for j in range(1, 13):
        mes.append(driver.find_element(By.XPATH,'//*[@id="cdk-overlay-2"]/div/mat-option[' + str(j) + ']').text)

    time.sleep(2)
    if driver.find_element(By.XPATH,'//*[@id="cdk-overlay-2"]/div/mat-option[' + str(mes.index(mes_ejemplo)+1) + ']').get_attribute('aria-disabled')=='true':
        driver.quit()
        print(mes_ejemplo + '-'+ ano_ejemplo + ' del proceso '+ proceso_ejemplo + ' No existe. Proceso finalizado ...')
        time.sleep(1)
        return

    driver.find_element(By.XPATH,'//*[@id="cdk-overlay-2"]/div/mat-option[' + str(mes.index(mes_ejemplo)+1) + ']').click()
    time.sleep(2)
    
    try:
            driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/div/mat-card/div[2]/div[2]/mat-paginator/div/div/div[2]/div')
    except:      
            driver.quit()
            print('No existen documentos para búsqueda realizada. Proceso finalizado ...')
            time.sleep(1)
            return

    

    ruta_proceso = ruta+'\\'+ str(proceso_ejemplo)
    ruta_ano = ruta_proceso +'\\'+ str(ano_ejemplo)
    ruta_mes = ruta_ano +'\\'+ str(mes_ejemplo)

    try:
        os.stat(ruta_proceso)
    except:
        os.mkdir(ruta_proceso)
        print('directorio del proceso ',proceso_ejemplo,' creado ... ', ruta_proceso)
    else:
        print('directorio del proceso ',proceso_ejemplo,' seleccionado...  ', ruta_proceso)
    
    try:
        os.stat(ruta_ano)
    except:
        os.mkdir(ruta_ano)
        print('directorio del año ',ano_ejemplo,' del proceso ',proceso_ejemplo,' creado... ', ruta_ano)
    else:
        print('directorio del año ',ano_ejemplo,' del proceso ',proceso_ejemplo,' seleccionado... ', ruta_ano)
    
    try:
        os.stat(ruta_mes)
    except:
        os.mkdir(ruta_mes)
        print('directorio del mes ',mes_ejemplo ,' del ',ano_ejemplo,' del proceso ',proceso_ejemplo,' creado... ', ruta_mes)


    time.sleep(5)
 

    driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/div/mat-card/div[2]/div[2]/mat-paginator/div/div/div[1]/mat-form-field').click()
    largo=driver.find_elements(By.XPATH,'//*[@id="cdk-overlay-3"]/div/mat-option/span[@class="mat-option-text"]')
  

    elemento=len(largo)
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="cdk-overlay-3"]/div/mat-option['+str(elemento)+']').click()
    time.sleep(5)

    paginas=driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/div/mat-card/div[2]/div[2]/mat-paginator/div/div/div[2]/div').text
    time.sleep(2)
    

    registros=int(paginas[paginas.index('of ')+3:])
    registrospp=int(paginas[paginas.index('- ')+2:paginas.index(' of')])
    registros_extra=registros%registrospp
  
    totalp=registros//registrospp + (1 if registros%registrospp>0 else 0)



    params = { 'behavior': 'allow', 'downloadPath': ruta_mes }
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

    if totalp==1:
        registros_extra=registrospp
    time.sleep(3)

    for i in range (1,totalp+1) :
        if i!=totalp:
            for j in range (1,registrospp) :
                version=driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/div/mat-card/div[1]/mat-expansion-panel['+str(j)+']/mat-expansion-panel-header/span/div[3]').text
                archivo_a_revisar=driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/div/mat-card/div[1]/mat-expansion-panel['+str(j)+']/mat-expansion-panel-header/span/div[6]').text
                if version[0:2]=="VE" and not(os.path.isfile(ruta_mes + '\\' + archivo_a_revisar)):
                    driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/div/mat-card/div[1]/mat-expansion-panel['+str(j)+']/mat-expansion-panel-header/span/div[7]/a').click()
                    print(ruta_mes+'\\'+archivo_a_revisar, '...descargado.')
                elif version[0:2]=="VE":
                    print('archivo ', archivo_a_revisar, 'ya existe. No descargado...')
                time.sleep(1)
        else:
            for j in range (1,registros_extra) :
                version=driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/div/mat-card/div[1]/mat-expansion-panel['+str(j)+']/mat-expansion-panel-header/span/div[3]').text
                archivo_a_revisar=driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/div/mat-card/div[1]/mat-expansion-panel['+str(j)+']/mat-expansion-panel-header/span/div[6]').text
                if version[0:2]=="VE" and not(os.path.isfile(ruta_mes + '\\' + archivo_a_revisar)):
                    driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/div/mat-card/div[1]/mat-expansion-panel['+str(j)+']/mat-expansion-panel-header/span/div[7]/a').click()
                    print(ruta_mes+'\\'+archivo_a_revisar, '...descargado.')
                elif version[0:2]=="VE":
                    print('archivo ', archivo_a_revisar, 'ya existe. No descargado...')
                time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="mat-tab-content-0-0"]/div/app-despliegue-publico/div/mat-card/div[2]/div[2]/mat-paginator/div/div/div[2]/button[2]').click()
        time.sleep(1)

    time.sleep(3)

    time.sleep(3)

    time.sleep(6)
    
    driver.quit()
    print('... archivos descargados...')
