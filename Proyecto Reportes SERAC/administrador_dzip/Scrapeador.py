from bs4 import BeautifulSoup
import os
import sqlite3
from timeit import default_timer
from config import conexion
from config import ejecutor
from config import save
import cProfile

 
#path de verificacion y comparación: "C:/Users/echirino/Documents/exel_descomprimidos_SERAC/report_date(08,03,2023)_time(11h34)-1.html"
path_carpeta=r"C:/Users/echirino/Documents/exel_descomprimidos_SERAC"
contador=0
for archivos in os.listdir(path_carpeta):
    nuevo_path= path_carpeta +'/'+ archivos
    with open(nuevo_path, 'rb') as f:
        contenido=f.read()
        #contenido_decodificado= contenido.decode('utf-8')
        contenido_decodificado = contenido.decode('utf-16', errors='ignore')
        soup= BeautifulSoup(contenido_decodificado, "lxml")  
            

        # el texto en a variable:
        #---------------------------------------------Tabla 1-------------------------------------------------------------------
        #Conexion con base de datos

        #conexion()
    inicio=default_timer()
    conector=conexion()
    #basededatos="C:\\Users\\echirino\\Documents\\Proyecto Reportes SERAC\\static\\db\\reportes_Serac.db"
    #conector=sqlite3.connect(basededatos)

    box=soup.find('div', class_="serac_header_data")

    nombre=box.find('td', class_='val'); nombre_valor= nombre.get_text()
    caudal= nombre.find_next('td', class_='val'); caudal_valor= caudal.get_text()
    #maquina= caudal.find_next('td', class_='val'); maquina_valor= maquina.get_text()

    #--------------------------------------------Tabla 2------------------------------------------------------------------
    box2=soup.find('div', class_='batch')

    refProd=box2.find('td', class_='val'); refProduccion_valor=refProd.get_text()
    if refProduccion_valor== "":
        print("no hago nada")
        pass
    else:
        refLot= refProd.find_next('td', class_='val'); refLote_valor= refLot.get_text()
        usuario= refLot.find_next('td', class_='val'); usuario_valor= usuario.get_text()
        #↓la variable pivo la uso para almacenar una variable que no sera usada en la base de datos pero sirve
        #↓como referencia para el find_next() y encontrar el siguiente valor que si importa
        pivot= usuario.find_next('td', class_='val')
        cantidad= pivot.find_next('td', class_='val'); cantidad_producir_valor= cantidad.get_text()
        #------------------------------------------tabla3 (dosificacion)-------------------------------------------------
        box3=soup.find('div', class_= 'product_file_data')

        pivot=box3.find('td', class_='val')
        ficha_embalaje=pivot.find_next('td', class_='val'); ficha_embalaje_valor=ficha_embalaje.get_text()
        cadencia= ficha_embalaje.find_next('td', class_='val'); cadencia_valor= cadencia.get_text() + " Emb/min"
        nombre_dosificacion= cadencia.find_next('td', class_='val'); nombre_dosificacion_valor= nombre_dosificacion.get_text()
        identificacion= nombre_dosificacion.find_next('td', class_='val'); identificacion_valor= identificacion.get_text()
        consigna_dosificacion= identificacion.find_next('td', class_='val'); consigna_dosificacion_valor=consigna_dosificacion.get_text()+ " g"
        minimo_aceptable= consigna_dosificacion.find_next('td', class_='val'); minimo_aceptable_valor= minimo_aceptable.get_text() + " g"
        maximo_aceptable= minimo_aceptable.find_next('td', class_='val'); maximo_aceptable_valor= maximo_aceptable.get_text() + " g"

        tara_minima= maximo_aceptable.find_next('td', class_='val'); tara_minima_valor= tara_minima.get_text() + " g"

        tara_maxima=tara_minima.find_next('td', class_='val'); tara_maxima_valor= tara_maxima.get_text()+ " g"

        evolucion_peso=tara_maxima.find_next('td', class_='val'); evolucion_peso_valor=evolucion_peso.get_text() +" g/s"

        velocidad_arranque= evolucion_peso.find_next('td', class_='val'); velocidad_arranque_valor= velocidad_arranque.get_text()+ " Emb/min"

        nivel_producto= velocidad_arranque.find_next('td', class_='val'); nivel_producto_valor= nivel_producto.get_text()+ " mm" 

        tiempo_dosificacion= nivel_producto.find_next('td', class_='val'); tiempo_dosificacion_valor= tiempo_dosificacion.get_text()+ " s"

        porcentaje_anticipacion= tiempo_dosificacion.find_next('td', class_='val'); porcentaje_anticipacion_valor= porcentaje_anticipacion.get_text() + " %"

        porcentaje_inicializacion= porcentaje_anticipacion.find_next('td', class_='val'); porcentaje_inicializacion_valor= porcentaje_inicializacion.get_text()+ " %"

        abertura_grancaudal= porcentaje_inicializacion.find_next('td', class_='val'); abertura_grancaudal_valor= abertura_grancaudal.get_text() + " s"

        cierre_grancaudal= abertura_grancaudal.find_next('td', class_='val'); cierre_grancaudal_valor= cierre_grancaudal.get_text()+ " %"
        fecha_hora_op= caudal_valor + " -- " + refProduccion_valor
        fecha_hora_op= fecha_hora_op.replace(" ", "")
        fecha_hora_op= fecha_hora_op.replace("/","-")
        arg= (nombre_dosificacion_valor, identificacion_valor, consigna_dosificacion_valor, minimo_aceptable_valor, maximo_aceptable_valor, tara_minima_valor, tara_maxima_valor, evolucion_peso_valor, velocidad_arranque_valor, nivel_producto_valor, tiempo_dosificacion_valor, porcentaje_anticipacion_valor, porcentaje_inicializacion_valor, abertura_grancaudal_valor, cierre_grancaudal_valor, refProduccion_valor, refLote_valor, fecha_hora_op)
        contador +=1
        ejecutor('dosificacion', arg, conector, "insertar")
        
        save(conector)
        print(f"------------------------------Listo tabla de dosificación del {contador}------------------------------")
        #------------------------------------------------Tabla Referencia_produccion---------------------------------------------------------------------------------------------------
        arg= (nombre_valor, caudal_valor, refProduccion_valor, refLote_valor, usuario_valor, cantidad_producir_valor, cadencia_valor, ficha_embalaje_valor, fecha_hora_op)
        ejecutor('referencia_produccion', arg, conector, "insertar")
        save(conector)
        print(f"------------------------------Listo tabla de referencia_produccion del {contador}------------------------------")
        #------------------------------------------Scraping eventos de producción------------------------------------------------------------------------------------------

        main= soup.find_all('div', id= 'main')
        for elemento in main:
            clase_mci= elemento.find_all('div', class_=['mci', 'mci_stopcause','filling_monitoring', 'fill_def', 'zero_scale_calibration'])
            for element in clase_mci:
                texto=element.get_text()
                if "\n" in texto:
                    texto = texto.split("\n")
                    texto = [elem for elem in texto if bool(elem)]
                else:
                    texto=texto.split(sep=",")
                texto_len= len(texto)

                if texto_len ==2:
                    evento= texto[1]
                    fecha_y_hora=texto[0]
                    #Conexion con base de datos
                    arg= (evento, fecha_y_hora, refProduccion_valor, fecha_hora_op)
                    ejecutor( "Eventos", arg, conector, "insertar")
                    
                elif texto_len==3 and 'Puesta a cero de las balanzas' in texto:
                    evento=texto[0]
                    fecha_y_hora=texto[1]
                    texto_descripcion=texto[2]
                    arg=(evento, fecha_y_hora, texto_descripcion, refProduccion_valor, fecha_hora_op )
                    ejecutor( 'Eventos2', arg, conector, "insertar")
                elif texto_len==3:
                    evento= texto[1]
                    fecha_y_hora=texto[0]
                    texto_descripcion= texto[2]
                    #Conexion con base de datos
                    arg=(evento, fecha_y_hora, texto_descripcion, refProduccion_valor, fecha_hora_op )
                    ejecutor( 'Eventos2', arg, conector, "insertar")
            save(conector)
        print(f"------------------------------Listo tabla de eventos del {contador}------------------------------")
                                    
        #------------------------------------------Scraping para tabla de "Alarmas_reportes"----------------------------------------------------------------------------------------
        footer=soup.find('div', id='footer')
        alarmas=footer.find('div', class_='mci_no_stop_counter')
        table= alarmas.find('table')
        
        filas = table.find_all('tr')

        i=0
        for fila in filas:
            if i==0:
                i+=1
                continue
            celdas = fila.find_all(['td', 'th'])
            celdas_texto = [celda.text for celda in celdas]
            texto_len=len(celdas_texto)
            if texto_len ==4:
                enunciado= celdas_texto[0]
                cantidad_apariciones= celdas_texto[1]
                duracion_aparicion= celdas_texto[2]
                duracion_total_activacion= celdas_texto[3]
                arg=(enunciado, cantidad_apariciones, duracion_aparicion, duracion_total_activacion, refProduccion_valor, fecha_hora_op)
                ejecutor( 'alarmas_reportes', arg, conector, "insertar")
        save(conector)    
        print(f"------------------------------Listo tabla de alarmas_reportes {contador}------------------------------")
        #------------------------------------------Scraping para tabla de "defectos_dosificacion"------------------------------------------------------------------------------------------
        footer=soup.find('div', id='footer')
        alarmas=footer.find('div', class_='filling_defect_counter')
        if alarmas is not None:
            table= alarmas.find('table')
            filas = table.find_all('tr')
            i=0
            for fila in filas:
                if i==0 :
                    i+=1
                    continue
                elif i==1:
                    i+=1
                    continue
                celdas = fila.find_all(['td', 'th'])
                celdas_texto = [celda.text for celda in celdas]
                texto_len=len(celdas_texto)
                if texto_len ==6:
                    enunciado= celdas_texto[0]
                    cantidad_apariciones= celdas_texto[1]
                    numero_causa_no_produccion= celdas_texto[3]
                    duracion_con_presenciaDefectos= celdas_texto[4]
                    duracion_sin_presenciaDefectos= celdas_texto[5]
                    arg= (refProduccion_valor, enunciado, cantidad_apariciones, numero_causa_no_produccion, duracion_con_presenciaDefectos, duracion_sin_presenciaDefectos, fecha_hora_op)
                    ejecutor( 'defectos_dosificacion', arg, conector, "insertar")
            save(conector)
            print(f"------------------------------Listo tabla de defectos_dosificacion del {contador}------------------------------")
        else:
            print(f"no se encontró filling_defect_counter en la tabla defectos_dosificacion del numero {contador}, con la op {refProduccion_valor} ")
            enunciado="NULL"
            cantidad_apariciones= "NULL"
            numero_causa_no_produccion= "NULL"
            duracion_con_presenciaDefectos= "NULL"
            duracion_sin_presenciaDefectos= "NULL"
            arg= (refProduccion_valor, enunciado, cantidad_apariciones, numero_causa_no_produccion, duracion_con_presenciaDefectos, duracion_sin_presenciaDefectos, fecha_hora_op)
            ejecutor( 'defectos_dosificacion', arg, conector, "insertar")
            save(conector)
        
        #------------------------------------------Scraping para tabla de "estadisticas de dosificacion"------------------------------------------------------------------------------------------

        estats= soup.find('div', class_='filling_stat_end')
        fecha_estadisticas_dosificacion= estats.find('div', class_='date'); fecha_estadisticas_dosificacion_valor= fecha_estadisticas_dosificacion.get_text()
        table= estats.find('table')
        filas = table.find_all('tr')
        i=0
        for fila in filas:
            if i==0 :
                i+=1
                continue
            celdas = fila.find_all(['td', 'th'])
            celdas_texto = [celda.text for celda in celdas]
            texto_len=len(celdas_texto)
            if texto_len ==4:
                pico= celdas_texto[0]
                media= celdas_texto[1]
                diferencia_tipo= celdas_texto[2]
                poblacion= celdas_texto[3]
                arg= (refProduccion_valor, pico, media, diferencia_tipo, poblacion, fecha_estadisticas_dosificacion_valor, fecha_hora_op)
                ejecutor( 'Estadisticas_dosificacion', arg, conector, "insertar")
        save(conector)
        print(f"------------------------------Listo tabla de Estadisticas_dosificacion del {contador}------------------------------")
        #---------------------------------------------------------Siguiente tabla de peso neto----------------------------------------        
        table= estats.find('table', class_="shaft_stat")
        filas = table.find_all('tr')
        i=0
        for fila in filas:
            if i==0 :
                i+=1
                continue
            celdas = fila.find_all(['td', 'th'])
            celdas_texto = [celda.text for celda in celdas]
            texto_len=len(celdas_texto)
            if texto_len ==6:
                consigna_g= celdas_texto[0]
                media_G=celdas_texto[1]
                diferencia_tipo_g= celdas_texto[2]
                poblacion= celdas_texto[3]
                minimo_g=celdas_texto[4]
                maximo_g=celdas_texto[5]
                arg=(refProduccion_valor, consigna_g ,  media_G, diferencia_tipo_g, poblacion, minimo_g, maximo_g, fecha_estadisticas_dosificacion_valor, fecha_hora_op )
                ejecutor('Peso_neto', arg, conector, "insertar")
        save(conector)
        print(f"------------------------------Listo tabla de peso_neto {contador}------------------------------")
        #---------------------------------------------------------Siguiente tabla tara----------------------------------------        
        table= estats.find('table', class_="stat_tare")
        filas = table.find_all('tr')
        i=0
        for fila in filas:
            if i==0 :
                i+=1
                continue
            celdas = fila.find_all(['td', 'th'])
            celdas_texto = [celda.text for celda in celdas]
            texto_len=len(celdas_texto)
            if texto_len ==5:
                    media_G=celdas_texto[0]
                    diferencia_tipo_g= celdas_texto[1]
                    poblacion= celdas_texto[2]
                    minimo_g=celdas_texto[3]
                    maximo_g=celdas_texto[4]
                    arg=(refProduccion_valor, media_G, diferencia_tipo_g, poblacion, minimo_g, maximo_g, fecha_estadisticas_dosificacion_valor, fecha_hora_op )
                    ejecutor('Tara', arg, conector, "insertar")
        save(conector)
        print(f"------------------------------Listo tabla de tara {contador}------------------------------")
        #-------------------------------------------------------Tabla de tiempos de dosificacion----------------------------------------------------------------------------------------------------------------
        table= estats.find('table', class_="shaft_stat_time")
        filas = table.find_all('tr')
        i=0
        for fila in filas:
            if i==0 :
                i+=1
                continue
            celdas = fila.find_all(['td', 'th'])
            celdas_texto = [celda.text for celda in celdas]
            texto_len=len(celdas_texto)
            if texto_len ==5:
                media_s=celdas_texto[0]
                diferencia_tipo_s= celdas_texto[1]
                poblacion= celdas_texto[2]
                minimo_s=celdas_texto[3]
                maximo_s=celdas_texto[4]
                arg=(refProduccion_valor, media_s, diferencia_tipo_s, poblacion, minimo_s, maximo_s, fecha_estadisticas_dosificacion_valor, fecha_hora_op )
                ejecutor('Tiempo_dosificacion', arg, conector, "insertar")
        save(conector)
        print(f"------------------------------Listo tabla de tiempo_dosificaion del {contador}------------------------------")
        #---------------------------------------------alarmas que provocan la parada-------------------------------------------------------------
        box=footer.find('div', class_='mci_stop_cause_counter')
        table= box.find('table', class_='h2_in_table')
        filas = table.find_all('tr')
        i=0
        for fila in filas:
            if i==0 :
                i+=1
                continue
            elif i==1:
                i+=1
                continue
            celdas = fila.find_all(['td', 'th'])
            celdas_texto = [celda.text for celda in celdas]
            texto_len=len(celdas_texto)
            if texto_len ==6:
                enunciado=celdas_texto[0]
                cantidad_de_apariciones= celdas_texto[1]
                duracion_total_aparicion= celdas_texto[2]
                numero_causa_no_produccion=celdas_texto[3]
                duracion_no_produccion_con_presencia_defectos=celdas_texto[4]
                duracion_no_produccion_sin_presencia_defectos=celdas_texto[5]
                arg= (refProduccion_valor, enunciado, cantidad_de_apariciones, duracion_total_aparicion, numero_causa_no_produccion, duracion_no_produccion_con_presencia_defectos, duracion_no_produccion_sin_presencia_defectos, fecha_hora_op )
                ejecutor('Alarmas_que_provocan_parada', arg, conector, "insertar")
        save(conector)
        print(f"------------------------------Listo tabla de Alarmas_que_provocan_parada del {contador}------------------------------")
                    
        #------------------------------------------Alarmas que provocan el cierre del portillo------------------------------------------------------     
        box=footer.find('div', class_='mci_close_cause_counter')
        table= box.find('table', class_='h2_in_table')
        filas = table.find_all('tr')
        i=0
        for fila in filas:
            if i==0 :
                i+=1
                continue
            elif i==1:
                i+=1
                continue
            celdas = fila.find_all(['td', 'th'])
            celdas_texto = [celda.text for celda in celdas]
            texto_len=len(celdas_texto)
            if texto_len ==6:
                enunciado=celdas_texto[0]
                cantidad_de_apariciones= celdas_texto[1]
                duracion_total_aparicion= celdas_texto[2]
                numero_causa_no_produccion=celdas_texto[3]
                duracion_no_produccion_con_presencia_defectos=celdas_texto[4]
                duracion_no_produccion_sin_presencia_defectos=celdas_texto[5]
                arg=(refProduccion_valor, enunciado, cantidad_de_apariciones, duracion_total_aparicion, numero_causa_no_produccion, duracion_no_produccion_con_presencia_defectos, duracion_no_produccion_sin_presencia_defectos, fecha_hora_op )
                ejecutor('Alarmas_provocan_cierre_del_portillo', arg, conector, "insertar")
        save(conector)
        print(f"------------------------------Listo tabla de Alarmas_provocan_cierre_del_portillo del  {contador}------------------------------")
        #--------------------------------------------------------------------Resumen-------------------------------------------------------resumen=soup.find('div', class_= 'serac_footer')
        resumen=soup.find('div', class_= 'serac_footer')
        table= resumen.find('table')
        filas = table.find_all('tr')
        a=[]
        for fila in filas:
            celdas = fila.find_all('td', class_="val")
            for texto in celdas:
                a.append(texto.text)
        ficha_produccion= a[0]
        comienzo_produccion= a[1]
        fin_produccion=a[2]
        duracion_produccion= a[3]
        embalaje_bueno= a[4]
        embalaje_malo= a[5]

        resumen2= resumen.find('div', class_='histogram')
        table= resumen2.find('table')
        filas = table.find_all('tr')
        b=[]
        for fila in filas:
            span=fila.find_all('span')
            for texto in span:
                b.append(texto.text)
        duracion_preparacion= b[0]
        duracion_acumulada_produccion=b[1]
        duracion_acumulada_no_producccion= b[2]+ "+" + b[3]
        arg=(refProduccion_valor, refLote_valor, ficha_produccion, comienzo_produccion, fin_produccion, duracion_produccion, embalaje_bueno, embalaje_malo, duracion_preparacion, duracion_acumulada_produccion, duracion_acumulada_no_producccion, fecha_hora_op )
        ejecutor('resumen', arg, conector, "insertar")
        save(conector)
        print(f"------------------------------Listo tabla de resumen del {contador}------------------------------")
#--------------------------------------------------------------------contadores mantenimiento-------------------------------------------------------resumen=soup.find('div', class_= 'serac_footer')
        contador_mantenimiento=soup.find('div', class_= 'maint_cnt')
        if contador_mantenimiento is None:
            pass
        else:
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
            print(f"------------------------------Listo tabla de contador de mantenimiento del {contador}------------------------------")
        
        #-----------------------------------Defectos_dosificacion-------------------------------------- 
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

            contar=1
            for item in c:
                #defet0=item[0]; defect1=item[1]; defect2=item[2]; defect3=item[3]; defect4=item[4]; defect5
                arg=(refProduccion_valor, contar, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15], fecha_hora_op)
                contar+=1
                ejecutor('defectos_dosificacion_pico', arg, conector, "insertar")
            save(conector)
        print(f"------------------------------Listo tabla defectos_dosificacion del {contador}------------------------------")
        print(f"listo el archivo numero: {contador}")
        fin= default_timer()
        duracion_tiempo= fin-inicio
        print(duracion_tiempo)