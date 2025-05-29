from flask import Flask, render_template, url_for, jsonify, request, session
from flask_cors import CORS, cross_origin
from Modelos.EventoSismico import EventoSismico
from ListaEventosSismicos import ListarEventosSismicos
from GestorRevisionManual import GestorRevisionManual
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
global usuario 
usuario = "Bauti"  # Variable global para el usuario logueado


app = Flask(__name__, template_folder='../FRONTEND/templates', static_folder='../FRONTEND/static')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Para pruebas, usa "*" (luego restringe)

eventos_cache = None
gestor =  GestorRevisionManual()

# Lista persistente de eventos (en memoria)
eventos_persistentes = ListarEventosSismicos.crear_eventos_sismicos()

# Ruta para la página principal
@app.route('/')
def inicio():
    return render_template('index.html')

# @app.route('/registrarRevision')
# def retornarDatos():
#     # Usar la lista persistente y filtrar solo los auto-detectados
#     result = gestor.buscarEventosAutoDetectados(eventos_persistentes)
#     return render_template('registrar.html', eventos=result)

@app.route('/eventos', methods=['POST'])
def seleccionar_evento():
    data = request.get_json()
    magnitud = data.get('magnitud')
    lat_epicentro = data.get('latEpicentro')
    long_epicentro = data.get('longEpicentro')
    lat_hipocentro = data.get('latHipocentro')
    long_hipocentro = data.get('longHipocentro')

    # Buscar en la lista persistente
    evento_seleccionado = next(
        (evento for evento in eventos_persistentes
         if float(evento.getValorMagnitud()) == float(magnitud)
         and float(evento.getLatitudEpicentro()) == float(lat_epicentro)
         and float(evento.getLongitudEpicentro()) == float(long_epicentro)
         and float(evento.getLatitudHipocentro()) == float(lat_hipocentro)
         and float(evento.getLongitudHipocentro()) == float(long_hipocentro)
        ),
        None
    )

    gestor.tomarSeleccionDeEvento(evento_seleccionado)

    return jsonify('succes')
    # if evento_seleccionado:
    #     return jsonify({'success': True, 'redirect': '/mostrar_datos_evento'})
    # else:
    #     return jsonify({'success': False, 'error': 'Evento no encontrado'}), 404

# @app.route('/mostrar_datos_evento')
# def mostrar_datos_evento():
#     return render_template('datos_evento.html')

@app.route('/api/eventos', methods=['GET'])
def api_eventos():
    # Usar la lista persistente
    result = gestor.buscarEventosAutoDetectados(eventos_persistentes)
    return jsonify(result)

@app.route('/obtener_datos_evento')
def obtener_datos_evento():
    evento = gestor.getGestorRevisionManualEventoSismicoSeleccionado()
    if not evento:
        print("No hay evento seleccionado")
        return jsonify({'success': False, 'error': 'No hay evento seleccionado'}), 404

    # Obtener datos principales y series temporales
    datos_evento = evento.obtenerDatosSismicos()
    series_temporales = evento.obtenerSeriesTemporales()

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

@app.route('/api/alcances', methods=['GET'])
def api_alcances():
    alcances = ListarEventosSismicos.obtener_alcances()
    # Devuelve una lista de dicts con nombre y descripcion
    return jsonify([{'nombre': a.getNombre(), 'descripcion': a.getDescripcion()} for a in alcances])

@app.route('/api/origenes', methods=['GET'])
def api_origenes():
    origenes = ListarEventosSismicos.obtener_origenes()
    return jsonify([{'nombre': o.getNombre(), 'descripcion': o.getDescripcion()} for o in origenes])

@app.route('/modificar_datos_evento', methods=['POST'])
def modificar_datos_evento():
    evento = gestor.getGestorRevisionManualEventoSismicoSeleccionado()
    if not evento:
        return jsonify({'success': False, 'error': 'No hay evento seleccionado'}), 404
    data = request.json
    if 'valorMagnitud' in data:
        evento.setValorMagnitud(data['valorMagnitud'])
    if 'alcanceSismo' in data:
        # Buscar el objeto AlcanceSismo por nombre
        alcances = ListarEventosSismicos.obtener_alcances()
        alcance = next((a for a in alcances if a.getNombre() == data['alcanceSismo']), None)
        if alcance:
            evento.setAlcanceSismo(alcance)
    if 'origenGeneracion' in data:
        # Buscar el objeto OrigenDeGeneracion por nombre
        origenes = ListarEventosSismicos.obtener_origenes()
        origen = next((o for o in origenes if o.getNombre() == data['origenGeneracion']), None)
        if origen:
            evento.setOrigenGeneracion(origen)
    return jsonify({'success': True})

@app.route('/ejecutar_accion', methods=['POST'])
def ejecutar_accion():
    evento = gestor.getGestorRevisionManualEventoSismicoSeleccionado()
    if not evento:
        return jsonify({'success': False, 'error': 'No hay evento seleccionado'}), 404

    data = request.get_json()
    accion = data.get('accion')

    if accion == 'rechazar':
        global usuario
        estado_rechazado = gestor.obtenerEstadoRechazado()
        usuario_actual = usuario
        usuario_obj = gestor.buscarASLogueado(usuario_actual)
        gestor.validarDatosMinimosRequeridos(evento)
        gestor.rechazarEventoSismico(evento, usuario_obj, estado_rechazado)
        # El evento ya está en la lista persistente, solo cambia su estado
        return jsonify({'success': True, 'mensaje': 'Evento rechazado correctamente'})
    elif accion == 'confirmar':
        # Lógica para confirmar el evento
        # Aquí podrías actualizar el estado del evento en eventos_persistentes si es necesario
        return jsonify({'success': True, 'mensaje': 'Evento confirmado correctamente'})
    elif accion == 'experto':
        # Lógica para solicitar revisión a experto
        # Aquí podrías actualizar el estado del evento en eventos_persistentes si es necesario
        return jsonify({'success': True, 'mensaje': 'Revisión a experto solicitada'})
    else:
        return jsonify({'success': False, 'error': 'Acción no válida'}), 400

# ---------------------- INICIO DE LA APLICACIÓN ----------------------

if __name__ == '__main__':
    # Ejecutar la aplicación Flask en modo debug
    app.run(host='127.0.0.1', port=5001, debug=True)
