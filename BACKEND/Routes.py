from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from ListaEventosSismicos import ListarEventosSismicos
from ListaSismografos import ListaSismografos
from GestorRevisionManual import GestorRevisionManual
from Modelos.Usuario import Usuario
from Modelos.Sesion import Sesion
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
global usuario 
usuario = Usuario('nico', '123', '2025')  # Variable global para el usuario logueado
usuario_logueado = Sesion('2024', '2026', usuario)  # Simulación de una sesión de usuario


app = Flask(__name__, static_folder='../FRONTEND/static')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Para pruebas, usa "*" (luego restringe)

eventos_cache = None
gestor =  GestorRevisionManual()

# Lista persistente de eventos (en memoria)

sismografos_persistentes = ListaSismografos.crear_sismografos(usuario)
eventos_persistentes = ListarEventosSismicos.crear_eventos_sismicos(sismografos_persistentes, usuario)
lista_alcances = ListarEventosSismicos.obtener_alcances()
lista_origenes = ListarEventosSismicos.obtener_origenes()
estados = ListarEventosSismicos.obtener_estados()

@app.route('/eventos', methods=['POST'])
def seleccionar_evento():
    data = request.get_json()
    global usuario

    datos_evento, series_temporales = gestor.tomarSeleccionDeEventoSismico(eventos_persistentes, sismografos_persistentes, data, usuario_logueado, estados)
    
    # Si tienes listas de alcances y origenes, pásalas también (puedes obtenerlas de tu modelo o mockearlas)
    alcances_sismo = ["Local", "Regional", "Global"]
    origenes_generacion = ["Tectónico", "Volcánico", "Artificial"]

    return jsonify({
        'success': True,
        'evento': datos_evento,
        'series_temporales': series_temporales,
        'alcances_sismo': alcances_sismo,
        'origenes_generacion': origenes_generacion
    })
    

@app.route('/api/eventos', methods=['GET'])
def api_eventos():
    # Usar la lista persistente
    result = gestor.opRegistrarResultadoRevisionManual(eventos_persistentes)
    return jsonify(result)

@app.route('/modificar_datos_evento', methods=['POST'])
@cross_origin()
def modificar_datos_evento():
    result = gestor.tomarOpcionModificacionDatos(request, lista_alcances, eventos_persistentes, lista_origenes)
    return result

@app.route('/ejecutar_accion', methods=['POST'])
@cross_origin()
def ejecutar_accion():
    data = request.get_json()
    global usuario  # Asegúrate de que 'usuario' esté definido globalmente
    return gestor.tomarSeleccionOpcionEvento(data, estados)

@app.route('/mapa', methods=['GET'])
def mapa():
    msj = gestor.tomarSeleccionDeOpcionMapa()
    return jsonify(msj)

# ---------------------- INICIO DE LA APLICACIÓN ----------------------

if __name__ == '__main__':
    # Ejecutar la aplicación Flask en modo debug
    app.run(host='127.0.0.1', port=5001, debug=True)
