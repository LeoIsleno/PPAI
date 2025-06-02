from flask import Flask, render_template, url_for, jsonify, request, session
from flask_cors import CORS, cross_origin
from Modelos.EventoSismico import EventoSismico
from ListaEventosSismicos import ListarEventosSismicos
from ListaSismografos import ListaSismografos
from GestorRevisionManual import GestorRevisionManual
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
global usuario 
usuario = "Bauti"  # Variable global para el usuario logueado


app = Flask(__name__, static_folder='../FRONTEND/static')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Para pruebas, usa "*" (luego restringe)

eventos_cache = None
gestor =  GestorRevisionManual()

# Lista persistente de eventos (en memoria)
eventos_persistentes = ListarEventosSismicos.crear_eventos_sismicos()
sismografos_persistentes = ListaSismografos.crearSismografos()


@app.route('/eventos', methods=['POST'])
def seleccionar_evento():
    data = request.get_json()
    global usuario

    datos_evento, series_temporales = gestor.tomarSeleccionDeEventoSismico(eventos_persistentes, sismografos_persistentes, data, usuario)
    
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
    evento = gestor._GestorRevisionManual__eventoSismicoSeleccionado
    if not evento:
        return jsonify({'success': False, 'error': 'No hay evento seleccionado'}), 404
    data = request.json
    if 'valorMagnitud' in data:
        evento.setValorMagnitud(data['valorMagnitud'])
    if 'alcanceSismo' in data:
        alcances = ListarEventosSismicos.obtener_alcances()
        alcance = next((a for a in alcances if a.getNombre() == data['alcanceSismo']), None)
        if alcance:
            evento.setAlcanceSismo(alcance)
    if 'origenGeneracion' in data:
        origenes = ListarEventosSismicos.obtener_origenes()
        origen = next((o for o in origenes if o.getNombre() == data['origenGeneracion']), None)
        if origen:
            evento.setOrigenGeneracion(origen)
    # --- Actualiza el evento en la lista persistente si es necesario ---
    for idx, ev in enumerate(eventos_persistentes):
        if ev is evento:
            eventos_persistentes[idx] = evento
            break
    return jsonify({'success': True})

@app.route('/ejecutar_accion', methods=['POST'])
@cross_origin()
def ejecutar_accion():
    evento = gestor.obtenerEventoSeleccionado()
    if not evento:
        return jsonify({'success': False, 'error': 'No hay evento seleccionado'}), 404

    data = request.get_json()
    global usuario  # Asegúrate de que 'usuario' esté definido globalmente
    return gestor.tomarSeleccionOpcionEvento(data, usuario)

# ---------------------- INICIO DE LA APLICACIÓN ----------------------

if __name__ == '__main__':
    # Ejecutar la aplicación Flask en modo debug
    app.run(host='127.0.0.1', port=5001, debug=True)
