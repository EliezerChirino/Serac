from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import flash
from wtforms.csrf.session import SessionCSRF
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import jsonify
import forms
from wtforms.widgets import html_params
import sqlite3
from sqlite3 import Error
from administrador_dzip.config import conexion
from administrador_dzip.config import ejecutor
from administrador_dzip.config import save

reportes_SeracBD="C:\\Users\\echirino\\Documents\\Proyecto Reportes SERAC\\static\\db\\reportes_Serac.db"

app = Flask(__name__)
app.secret_key = 'mi_clave'
csrf = SessionCSRF()


@app.route("/", methods = ["GET","POST"])
def login():
    titulo = "Inicio de sesion"
    login_form = forms.login(request.form)
    if request.method == "POST": #"and login_form.validate():"
        connect=sqlite3.connect(reportes_SeracBD)
        cursor= connect.cursor()
        usuario = login_form.usuario.data.lower()
        clave = login_form.clave.data
        return redirect(url_for('indice'))
    return render_template("Login.html", titulo=titulo,form = login_form)

@app.route("/indice", methods = ["GET"])
def indice():
    titulo = "Indice"
    connect=sqlite3.connect(reportes_SeracBD)
    cursor= connect.cursor()
    nombre=cursor.execute('SELECT * FROM referencia_produccion').fetchall()
    connect.close()
    return render_template("Indice.html", titulo=titulo, nombre=nombre)



@app.route("/reportes-<string:fecha_Hora_OP>", methods=[ "GET"])
def reportes(fecha_Hora_OP):
    titulo="reportes"
    arg=(fecha_Hora_OP,)
    conex=conexion()
    tabla_ref_Producc=ejecutor("referencia_produccion", arg, conex, "select")
    tabla_resumen= ejecutor("resumen", arg, conex, "select" )
    tabla_eventos= ejecutor("Eventos", arg, conex, "select_list") #Es select_list porque estoy tomando toda la lista y en el config utilizo el fecthall
    tabla_dosificacion=ejecutor('dosificacion', arg, conex, "select")
    tabla_estads_dosificacion=ejecutor('Estadisticas_dosificacion', arg, conex, "select_list")#Es select_list porque estoy tomando toda la lista y en el config utilizo el fecthall
    tabla_peso_neto= ejecutor("Peso_neto", arg, conex, "select_list" )#Es select_list porque estoy tomando toda la lista y en el config utilizo el fecthall
    tabla_tara= ejecutor("Tara", arg, conex, "select_list" )#Es select_list porque estoy tomando toda la lista y en el config utilizo el fecthall
    tabla_tiempo_dosificacion= ejecutor("Tiempo_dosificacion", arg, conex, "select_list" )#Es select_list porque estoy tomando toda la lista y en el config utilizo el fecthall
    tabla_alarmas_reportes= ejecutor("alarmas_reportes", arg, conex, "select_list" )
    tabla_defectos_dosificacion=ejecutor("defectos_dosificacion", arg, conex, "select_list" )
    tabla_eventos_que_provocan_paradas=ejecutor("Alarmas_que_provocan_parada", arg, conex, "select_list" ) 
    tabla_eventos_cierre_portillo=ejecutor("Alarmas_provocan_cierre_del_portillo", arg, conex, "select_list" ) 
    tabla_contadores_mantenimiento= ejecutor("contador_mantenimiento", arg, conex, "select_list" ) 
    tabla_picos=ejecutor("defectos_dosificacion_pico", arg, conex, "select_list" ) 
    
    #↓↓↓↓ -- Diccionario para la tabla de referencia de produccion -- ↓↓↓↓

    items_RefProduc={
        "Nombre" : tabla_ref_Producc[0],
        "caudal_produccion": tabla_ref_Producc[1],
        "OP": tabla_ref_Producc[2],
        "lote":  tabla_ref_Producc[3],    
        "usuario": tabla_ref_Producc[4],
        "cantidad_producc": tabla_ref_Producc[5],
        "cadencia": tabla_ref_Producc[6],
        "ficha_embalaje":tabla_ref_Producc[7]
        }
    items_resumen={
        "OP": tabla_resumen[0],
        "lote": tabla_resumen[1],
        "nombre_ficha_produccion": tabla_resumen[2],
        "Comienzo_produccion": tabla_resumen[3],
        "fin_produccion": tabla_resumen[4],
        "duracion": tabla_resumen[5],
        "cantidad_bueno": tabla_resumen[6],
        "cantidad_malo": tabla_resumen[7],
        "duracion_preparacion": tabla_resumen[8],
        "duracion_acumulada_produccion": tabla_resumen[9],
        "duracion_acumulada_no_producccion": tabla_resumen[10]
    }
    items_dosificacion={
        "nombre_dosificacion":tabla_dosificacion[0],
        "identificacion": tabla_dosificacion[1],
        "consigna": tabla_dosificacion[2],
        "minimo_aceptable": tabla_dosificacion[3],
        "maximo_aceptable": tabla_dosificacion[4], 
        "tara_minima": tabla_dosificacion[5],
        "tara_maxima": tabla_dosificacion[6],
        "evolucion_peso": tabla_dosificacion[7],
        "velocidad_arranque": tabla_dosificacion[8],
        "nivel_producto": tabla_dosificacion[9],
        "tiempo_dosificacion": tabla_dosificacion[10],
        "porcentaje_anticipacion": tabla_dosificacion[11],
        "porcentaje_inicializacion":tabla_dosificacion[12],
        "abertura_gran_caudal": tabla_dosificacion[13],
        "cierre_gran_caudal": tabla_dosificacion[14]
    }
    
    return render_template("tablas.html", titulo=titulo, items_RefProduc= items_RefProduc, items_resumen=items_resumen, tabla_eventos=tabla_eventos, items_dosificacion=items_dosificacion, tabla_estads_dosificacion=tabla_estads_dosificacion, tabla_peso_neto=tabla_peso_neto, tabla_tara=tabla_tara, tabla_tiempo_dosificacion=tabla_tiempo_dosificacion, tabla_alarmas_reportes=tabla_alarmas_reportes, tabla_defectos_dosificacion=tabla_defectos_dosificacion, tabla_eventos_que_provocan_paradas=tabla_eventos_que_provocan_paradas, tabla_eventos_cierre_portillo=tabla_eventos_cierre_portillo, tabla_contadores_mantenimiento=tabla_contadores_mantenimiento, tabla_picos=tabla_picos)

if __name__ == "__main__":
	app.run(debug=True, port=5000, host="0.0.0.0")
        
        