import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
from BACKEND.ListaEventosSismicos import ListarEventosSismicos
from BACKEND.ListaSismografos import ListaSismografos
from BACKEND.GestorRevisionManual import GestorRevisionManual
from BACKEND.Modelos.Usuario import Usuario
from BACKEND.Modelos.Empleado import Empleado
from BACKEND.Modelos.Rol import Rol
from BACKEND.Modelos.Sesion import Sesion
from BDD import database

# Usuario de prueba
usuario = Usuario('nico', '123', datetime(2025, 1, 1))
rol_admin = Rol('Administrador de Sismos', 'Rol con permisos para revisar eventos sísmicos')
empleado = Empleado('Nico', 'Apellido', 'nico@example.com', '123456789', rol_admin)
usuario.setEmpleado(empleado)
usuario_logueado = Sesion(datetime(2024, 1, 1), datetime(2026, 12, 31), usuario)

app = Flask(__name__, static_folder='../FRONTEND/static')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

gestor = GestorRevisionManual()

# Inicializar datos
try:
    database.init_db()
except Exception:
    pass

sismografos_persistentes = []
try:
    provider = ListaSismografos(usuario)
    sismografos_persistentes = getattr(provider, 'sismografos', []) or []
except Exception:
    pass

eventos_persistentes = []
try:
    eventos_persistentes = ListarEventosSismicos.crear_eventos_sismicos(sismografos_persistentes, usuario)
except Exception:
    pass

lista_alcances = []
try:
    lista_alcances = ListarEventosSismicos.obtener_alcances()
except Exception:
    pass

lista_origenes = []
try:
    lista_origenes = ListarEventosSismicos.obtener_origenes()
except Exception:
    pass

estados = []
try:
    estados = ListarEventosSismicos.obtener_estados()
except Exception:
    pass

@app.route('/eventos', methods=['POST'])
def seleccionar_evento():
    try:
        data = request.get_json()
        resultado = gestor.tomarSeleccionDeEventoSismico(
            eventos_persistentes,
            sismografos_persistentes,
            data,
            usuario_logueado,
            estados
        )
        
        if isinstance(resultado, dict) and not resultado.get('success', True):
            status = resultado.pop('status_code', 500)
            return jsonify(resultado), status
        
        if not isinstance(resultado, tuple):
            return jsonify({'success': False, 'error': 'Error inesperado'}), 500
        
        datos_evento, series_temporales = resultado
        
        return jsonify({
            'success': True,
            'evento': datos_evento,
            'series_temporales': series_temporales,
            'alcances_sismo': ["Local", "Regional", "Global"],
            'origenes_generacion': ["Tectónico", "Volcánico", "Artificial"]
        })
    except Exception as e:
        # Avoid printing/logging to console. Return a generic error to the caller.
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@app.route('/api/eventos', methods=['GET'])
def api_eventos():
    resultado = gestor.opRegistrarResultadoRevisionManual(eventos_persistentes)
    return jsonify(resultado)

@app.route('/modificar_datos_evento', methods=['POST'])
def modificar_datos_evento():
    resultado = gestor.tomarOpcionModificacionDatos(
        request,
        lista_alcances,
        eventos_persistentes,
        lista_origenes
    )
    
    if isinstance(resultado, dict) and not resultado.get('success', True):
        status = resultado.pop('status_code', 500)
        return jsonify(resultado), status
    
    return jsonify(resultado)

@app.route('/ejecutar_accion', methods=['POST'])
def ejecutar_accion():
    data = request.get_json()
    resultado = gestor.tomarSeleccionOpcionEvento(data, estados)
    
    if isinstance(resultado, dict) and not resultado.get('success', True):
        status = resultado.pop('status_code', 500)
        return jsonify(resultado), status
    
    return jsonify(resultado)

@app.route('/mapa', methods=['GET'])
def mapa():
    return jsonify(gestor.tomarSeleccionDeOpcionMapa())

@app.route('/')
def index():
    return send_from_directory('../FRONTEND', 'login.html')

@app.route('/index.html')
def dashboard():
    return send_from_directory('../FRONTEND', 'index.html')

@app.route('/<path:filename>')
def serve_html(filename):
    if filename.endswith('.html'):
        return send_from_directory('../FRONTEND', filename)
    return '', 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
