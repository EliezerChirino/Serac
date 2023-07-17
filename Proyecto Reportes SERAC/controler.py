import sqlite3 

def tabla1():
    connect=sqlite3.connect("reportes_Serac.db")
    try:
        cursor= connect.cursor()
        cursor.execute(""" CREATE TABLE Eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_evento VARCHAR(20),
            hora VARCHAR(20),
            descripcion VARCHAR(20),
            OP INTEGER
            )""")
        print("se creo la tabla Eventos")                        
    except sqlite3.OperationalError:
        print("La tabla Eventos ya existe")      
        connect.commit()
        connect.close()
    connect.close()
    
def tabla2():
    connect=sqlite3.connect("reportes_Serac.db")
    try:
        cursor= connect.cursor()
        cursor.execute(""" CREATE TABLE Estadisticas_dosificacion (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             pico INTEGER,
             media INTEGER,
             diferencia_tipo REAL,
             poblacion INTEGER, 
             OP INTEGER
            )""")
        print("se creo la tabla Estadisticas_dosificacion")                        
    except sqlite3.OperationalError:
        print("La tabla Estadisticas_dosificacion ya existe")      
        connect.commit()
        connect.close()
    connect.close()
    
def tabla3():
    connect=sqlite3.connect("reportes_Serac.db")
    try:
        cursor= connect.cursor()
        cursor.execute(""" CREATE TABLE Peso_neto (
             OP INTEGER PRIMARY KEY,
             consigna REAL, 
             media REAL,
             diferencia_tipoG REAL,
             poblacion INTEGER,
             minimo_G REAL,
             maximo_g REAL
             
            )""")
        print("se creo la tabla Peso_neto")                        
    except sqlite3.OperationalError:
        print("La tabla Peso_neto ya existe")      
        connect.commit()
        connect.close()
    connect.close()
    
def tabla4():
    connect=sqlite3.connect("reportes_Serac.db")
    try:
        cursor= connect.cursor()
        cursor.execute(""" CREATE TABLE Tara (
             OP INTEGER PRIMARY KEY,
             media REAL,
             diferencia_tipoG REAL,
             poblacion INTEGER,
             minimo_G REAL,
             maximo_g REAL
             
            )""")
        print("se creo la tabla Tara")                        
    except sqlite3.OperationalError:
        print("La tabla Tara ya existe")      
        connect.commit()
        connect.close()
    connect.close()
    
def tabla5():
    connect=sqlite3.connect("reportes_Serac.db")
    try:
        cursor= connect.cursor()
        cursor.execute(""" CREATE TABLE Tiempo_dosificacion (
             OP INTEGER PRIMARY KEY,
             media_S REAL,
             diferencia_S REAL,
             poblacion INTEGER,
             minimo_S REAL,
             maximo_S REAL
             
            )""")
        print("se creo la tabla Tiempo_dosificacion")                        
    except sqlite3.OperationalError:
        print("La tabla Tiempo_dosificacion ya existe")      
        connect.commit()
        connect.close()
    connect.close()
    
def tabla6():
    connect=sqlite3.connect("reportes_Serac.db")
    try:
        cursor= connect.cursor()
        cursor.execute(""" CREATE TABLE referencia_produccion (
             nombre_produccion VARCHAR(30),
             caudal_produccion VARCHAR(30),
             referencia_produccion VARCHAR (20),
             lote VARCHAR(20) PRIMARY KEY,
             nombre_usuario VARCHAR(20),
             cantidad INTEGER,
             cadencia INTEGER
             
            )""")
        print("se creo la tabla referencia_produccion")                        
    except sqlite3.OperationalError:
        print("La tabla referencia_produccion ya existe")      
        connect.commit()
        connect.close()
    connect.close()
    
def tabla7():
    connect=sqlite3.connect("reportes_Serac.db")
    try:
        cursor= connect.cursor()
        cursor.execute(""" CREATE TABLE resumen (
             OP INTEGER,
             lote INTEGER,
             fin_produccion VARCHAR (20),
             duracion VARCHAR(20),
             cantidad_bueno INTEGER,
             cantidad_malo INTEGER,
             duracion_preparacion VARCHAR(20),
             duracion_acumulada_produccion VARCHAR(20),
             duracion_acumulada_no_producccion VARCHAR(20)
             
            )""")
        print("se creo la tabla resumen")                        
    except sqlite3.OperationalError:
        print("La tabla resumen ya existe")      
        connect.commit()
        connect.close()
    connect.close()
    
def tabla8():
    connect=sqlite3.connect("reportes_Serac.db")
    try:
        cursor= connect.cursor()
        cursor.execute(""" CREATE TABLE alarmas_reportes (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             OP INTEGER,
             enunciado VARCHAR(30),
             cantidad_apariciones INTEGER,
             duracion_total VARCHAR(20),
             numero_causa_no_produccion INTEGER,
             con_presencia INTEGER,
             sinpresemcoa INTEGER,
             duracion_total_deactividad VARCHAR(20)
            )""")
        print("se creo la tabla alarmas_reportes")                        
    except sqlite3.OperationalError:
        print("La tabla alarmas_reportes ya existe")      
        connect.commit()
        connect.close()
    connect.close()
    
def tabla9():
    connect=sqlite3.connect("reportes_Serac.db")
    try:
        cursor= connect.cursor()
        cursor.execute(""" CREATE TABLE dosificacion (
             nombre_dosificacion VARCHAR(15),
             identificacion VARCHAR(15),
             consigna_dosificacion_G REAL,
             minimo_acepable_G REAL,
             maximo_aceptable_G REAL,
             tara_minima_G REAL,
             tara_maxima_G REAL, 
             evolucion_peso REAL,
             velocidad_arranque VARCHAR(12),
             nivel_producto VARCHAR(15),
             tiempo_dosificacion VARCHAR(20),
             porcentaje_anticipacion VARCHAR (12),
             porcentaje_inicializacion VARCHAR(12),
             abertura_caudal VARCHAR(12),
             cierra_grancaudal VARCHAR(12),
             OP INTEGER, 
             lote VARCHAR(15) PRIMARY KEY
             
            )""")
        print("se creo la tabla dosificacion")                        
    except sqlite3.OperationalError:
        print("La tabla dosificacion ya existe")      
        connect.commit()
        connect.close()
    connect.close()
    
def tabla10():
    connect=sqlite3.connect("reportes_Serac.db")
    try:
        cursor= connect.cursor()
        cursor.execute(""" CREATE TABLE usuarios (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre VARCHAR(15),
             apellido VARCHAR(15),
             username VARCHAR(15),
             password VARCHAR(15)
            )""")
        print("se creo la tabla usuarios")                        
    except sqlite3.OperationalError:
        print("La tabla usuarios ya existe")      
        connect.commit()
        connect.close()
    connect.close()
    
tabla1()
tabla2()
tabla3()
tabla4()
tabla5()
tabla6()
tabla7()
tabla8()
tabla9()
tabla10()
    
    
    