import sqlite3
ruta_bd="C:\\Users\\echirino\\Documents\\Proyecto Reportes SERAC\\static\\db\\reportes_Serac.db"

def conexion():
    conex= None
    try:
        conex=sqlite3.connect(ruta_bd)
    except Exception as e:
        raise ValueError("Error al conectar con la base de datos "+ str(e))
    return conex


def ejecutor(tabla, args, conex, accion ):
    if accion== "insertar":
        sql=insertar(tabla)
        result= False
        cursor=conex.cursor()
        try:
            cursor.execute(sql, args)
            result = True
        except Exception as e:
            print("Error al ejecutar consulta porque: " + str(e))
            pass
        return result
    elif accion== "select":
        sql=seleccionar(tabla)
        result= False
        cursor=conex.cursor()
        try:
            cursor.execute(sql, args)
            result = cursor.fetchone()
        except Exception as e:
            print("Error al ejecutar consulta porque: " + str(e))
            pass
        return result
    elif accion== "select_list":
        sql=seleccionar(tabla)
        result= False
        cursor=conex.cursor()
        try:
            cursor.execute(sql, args)
            result = cursor.fetchall()
        except Exception as e:
            print("Error al ejecutar consulta porque: " + str(e))
            pass
        return result
    
def insertar(tabla):
    if tabla== 'dosificacion':
        return('INSERT INTO dosificacion (nombre_dosificacion, identificacion, consigna_dosificacion_G, minimo_acepable_G, maximo_aceptable_G, tara_minima_G, tara_maxima_G, evolucion_peso, velocidad_arranque, nivel_producto, tiempo_dosificacion, porcentaje_anticipacion, porcentaje_inicializacion, abertura_caudal, cierra_grancaudal, OP, lote, fecha_Hora_OP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)' )   
    elif tabla== 'referencia_produccion':
        return('INSERT INTO referencia_produccion (nombre_produccion, caudal_produccion, referencia_produccion, lote, nombre_usuario, cantidad, cadencia, ficha_embalaje, fecha_Hora_OP ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)' )   
    elif tabla== "Eventos":
        return('INSERT INTO Eventos (tipo_evento, hora, OP, fecha_Hora_OP) VALUES (?, ?, ?, ?)' )   
    elif tabla== 'Eventos2':
        return('INSERT INTO Eventos (tipo_evento, hora, descripcion, OP, fecha_Hora_OP) VALUES (?, ?, ?, ?, ?)' )   
    elif tabla== 'alarmas_reportes':
        return('INSERT INTO alarmas_reportes (enunciado, cantidad_apariciones, duracion_total, duracion_total_activacion, OP, fecha_Hora_OP ) VALUES (?, ?, ?, ?, ?, ?)' )  
    elif tabla=='defectos_dosificacion':
        return('INSERT INTO defectos_dosificacion (OP, enunciado, cantidad_apariciones, numero_causa_no_produccion, duracion_con_presencia_defectos, duracion_sin_presencia_defectos, fecha_Hora_OP ) VALUES (?, ?, ?, ?, ?, ?, ?)')
    elif tabla=="Estadisticas_dosificacion":
        return("""INSERT INTO Estadisticas_dosificacion (OP, pico, media, diferencia_tipo, poblacion, fecha_estadistica_dosificacion, fecha_Hora_OP ) VALUES (?, ?, ?, ?, ?, ?, ?)""" ) 
    elif tabla== "Peso_neto":
        return('INSERT INTO Peso_neto (OP, consigna, media, diferencia_tipoG, poblacion, minimo_G, maximo_g, fecha_estadistica, fecha_Hora_OP  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)')
    elif tabla== 'Tara':
        return('INSERT INTO Tara (OP, media, diferencia_tipoG, poblacion, minimo_G, maximo_g, fecha_estadistica, fecha_Hora_OP ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
    elif tabla== 'Tiempo_dosificacion':
        return('INSERT INTO Tiempo_dosificacion (OP, media_S, diferencia_S, poblacion, minimo_S, maximo_S, fecha_estadistica, fecha_Hora_OP ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
    elif tabla== 'Alarmas_que_provocan_parada':
        return('INSERT INTO Alarmas_que_provocan_parada(OP, enunciado, cantidad_apariciones, duracion_total_aparicion, numero_causa_no_produccion, duracion_no_produccion_con_presencia_defectos, duracion_no_produccion_sin_presencia_defectos, fecha_Hora_OP ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
    elif tabla== 'Alarmas_provocan_cierre_del_portillo':
        return('INSERT INTO Alarmas_provocan_cierre_del_portillo(OP, enunciado, cantidad_apariciones, duracion_total_aparicion, numero_causa_no_produccion, duracion_acumulada_no_produccion_con_presencia_defectos, duracion_acumulada_no_produccion_sin_presencia_defectos, fecha_Hora_OP ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
    elif tabla== 'resumen':
        return('INSERT INTO resumen(OP, lote, nombre_ficha_produccion, comienzo_produccion, fin_produccion, duracion, cantidad_bueno, cantidad_malo, duracion_preparacion, duracion_acumulada_produccion, duracion_acumulada_no_producccion, fecha_Hora_OP) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
    elif tabla== 'defectos_dosificacion_pico':
        return('INSERT INTO defectos_dosificacion_pico(OP, pico, defecto_0, defecto_1, defecto_2, defecto_3, defecto_4, defecto_5, defecto_6, defecto_7, defecto_8, defecto_9, defecto_10, defecto_11, defecto_12, defecto_13, defecto_14, defecto_15, fecha_hora_op ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ? , ?, ?, ?, ?, ? )')
    elif tabla== 'contador_mantenimiento':
        return('INSERT INTO contador_mantenimiento(OP, descripcion, valor, fecha_hora_op ) VALUES(?, ?, ?, ? )')

def seleccionar(tabla):
    if tabla=='referencia_produccion':
        return('SELECT * FROM referencia_produccion WHERE fecha_Hora_OP = ?')
    elif tabla=='resumen': 
        return('SELECT * FROM resumen where fecha_Hora_OP = ?')
    elif tabla=='Eventos':
        return('SELECT * FROM Eventos where fecha_Hora_OP = ?')
    elif tabla=="dosificacion":
        return('SELECT * FROM dosificacion where fecha_Hora_OP = ?')
    elif tabla=="Estadisticas_dosificacion":
        return('SELECT * FROM Estadisticas_dosificacion where fecha_Hora_OP = ?')
    elif tabla=="Peso_neto":
        return('SELECT * FROM Peso_neto where fecha_Hora_OP = ?')
    elif tabla=="Tara":
        return('SELECT * FROM Tara where fecha_Hora_OP = ?')
    elif tabla=="Tiempo_dosificacion":
        return('SELECT * FROM Tiempo_dosificacion where fecha_Hora_OP = ?')
    elif tabla=="alarmas_reportes":
        return('SELECT * FROM alarmas_reportes where fecha_Hora_OP = ?')
    elif tabla=="defectos_dosificacion":
        return('SELECT * FROM defectos_dosificacion where fecha_Hora_OP = ?')
    elif tabla == "Alarmas_que_provocan_parada":
        return('SELECT * FROM Alarmas_que_provocan_parada where fecha_Hora_OP = ?')
    elif tabla== "Alarmas_provocan_cierre_del_portillo":
        return('SELECT * FROM Alarmas_provocan_cierre_del_portillo where fecha_Hora_OP = ?')
    elif tabla== 'contador_mantenimiento':
        return('SELECT * FROM contador_mantenimiento where fecha_Hora_OP = ?')
    elif tabla=='defectos_dosificacion_pico':
        return('SELECT * FROM defectos_dosificacion_pico where fecha_Hora_OP = ?')
    

def save(conex):
    conex.commit()

def close(conex):
    conex.close()
