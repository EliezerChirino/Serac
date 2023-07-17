from bs4 import BeautifulSoup
import os
import sqlite3
from timeit import default_timer
from config import conexion
from config import ejecutor
from config import save
import cProfile

with open("C:/Users/echirino/Documents/exel_descomprimidos_SERAC/report_date(23,05,2022)_time(10h14)-1.html", 'rb') as f:
        contenido=f.read()
        #contenido_decodificado= contenido.decode('utf-8')
        contenido_decodificado = contenido.decode('utf-16', errors='ignore')
        soup= BeautifulSoup(contenido_decodificado, "lxml")  
conector=conexion()
""""

refProduccion_valor=1
fecha_hora_op=2
contador_mantenimiento=soup.find('div', class_= 'maint_cnt')
if contador_mantenimiento is not None:
    table= contador_mantenimiento.find('table')
    filas = table.find_all('tr')
    for fila in filas:
        cont= fila.find_all('td', class_=['txt', 'val'])
        lista= [celda.text for celda in cont]
        descripcion=lista[0]
        valor= lista[1]
        arg=(refProduccion_valor, descripcion, valor, fecha_hora_op)
        ejecutor('contador_mantenimiento', arg, conector, "insertar")
        save(conector)
else:
    pass"""
    

      
defectos_dosificacion_picos = soup.find_all('div', class_='filling_defect_counter')
b=[]
c=[]
if len(defectos_dosificacion_picos)==0:
    pass
else:
    if len(defectos_dosificacion_picos) > 1:
        pivot = defectos_dosificacion_picos[1]
    else:
        pivot = defectos_dosificacion_picos[0]
    table = pivot.find('table', class_="defect_per_station")
    filas = table.find_all('tr')
    lista= [celda.text for celda in filas]
    lista.pop(0)
    listap= lista[0]
    cont=0
    for elem in lista:
        
        for x in elem:
            b.append(x)
        a= len(b)
        if a ==17:
            del b[0]
        elif a>17:
            del b[0]
            del b[0]
                    
        c.append(b)
        b=[]
    print(c)
    i=1
    for item in c:
        
        refProduccion_valor=1
        
        #defet0=item[0]; defect1=item[1]; defect2=item[2]; defect3=item[3]; defect4=item[4]; defect5
        arg=(refProduccion_valor, i, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15], i)
        i+=1
        ejecutor('defectos_dosificacion_pico', arg, conector, "insertar")
        save(conector)
        
    
        
    
     
     

    
"""
    picos={
        'pico1': [],
        'pico2': [],
        'pico3': [],
        'pico4': [],
        'pico5': [],
        'pico6': [],
        'pico7': [],
        'pico8': [],
        'pico9': [],
        'pico10': [],
        'pico11': [],
        'pico12': []
    }
     
    picos['pico1'].append(lista[0])
    picos['pico2'].append(lista[1])
    picos['pico3'].append(lista[2])
    picos['pico4'].append(lista[3])
    picos['pico5'].append(lista[4])
    picos['pico6'].append(lista[5]) 
    picos['pico7'].append(lista[6])
    picos['pico8'].append(lista[7])
    picos['pico9'].append(lista[8])
    picos['pico10'].append(lista[9])
    picos['pico11'].append(lista[10])
    picos['pico12'].append(lista[11]) 
    cont=1
    #for pico in picos:

   
        
    print(picos['pico1'][0][0])
    """
"""caracteres_separados = ", ".join([char for palabra in picos['pico'+str(cont)] for char in palabra])
        print(caracteres_separados[0])"""

        