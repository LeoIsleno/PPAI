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

# Configuración del usuario logueado
usuario = Usuario('nico', '123', datetime(2025, 1, 1))
rol_admin = Rol('Administrador de Sismos', 'Rol con permisos para revisar eventos sísmicos')
empleado_nico = Empleado('Nico', 'Apellido', 'nico@example.com', '123456789', rol_admin)
usuario.setEmpleado(empleado_nico)
usuario_logueado = Sesion(datetime(2024, 1, 1), datetime(2026, 12, 31), usuario)

app = Flask(__name__, static_folder='../FRONTEND/static')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

gestor = GestorRevisionManual()

# Inicializar base de datos y cargar datos
try:
    database.init_db()
except Exception:
    pass

try:
    sismografos_provider = ListaSismografos(usuario)
    sismografos_persistentes = getattr(sismografos_provider, 'sismografos', []) or []
except Exception:
    sismografos_persistentes = []

try:
    eventos_persistentes = ListarEventosSismicos.crear_eventos_sismicos(sismografos_persistentes, usuario)
except Exception:
    eventos_persistentes = []

try:
    lista_alcances = ListarEventosSismicos.obtener_alcances()
except Exception:
    lista_alcances = []

try:
    lista_origenes = ListarEventosSismicos.obtener_origenes()
except Exception:
    lista_origenes = []

try:
    estados = ListarEventosSismicos.obtener_estados()
except Exception:
    estados = []

@app.route('/eventos', methods=['POST'])
def seleccionar_evento():
    try:
        data = request.get_json()
        resultado = gestor.tomarSeleccionDeEventoSismico(eventos_persistentes, sismografos_persistentes, data, usuario_logueado, estados)
        
        if isinstance(resultado, dict) and not resultado.get('success', True):
            status_code = resultado.pop('status_code', 500)
            return jsonify(resultado), status_code
        
        if isinstance(resultado, tuple):
            datos_evento, series_temporales = resultado
        else:
            return jsonify({'success': False, 'error': 'Error inesperado al seleccionar evento'}), 500
        
        alcances_sismo = ["Local", "Regional", "Global"]
        origenes_generacion = ["Tectónico", "Volcánico", "Artificial"]

        return jsonify({
            'success': True,
            'evento': datos_evento,
            'series_temporales': series_temporales,
            'alcances_sismo': alcances_sismo,
            'origenes_generacion': origenes_generacion
        })
    except Exception as e:
        print(f"ERROR en seleccionar_evento: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Error del servidor: {str(e)}'}), 500
    

@app.route('/api/eventos', methods=['GET'])
def api_eventos():
    result = gestor.opRegistrarResultadoRevisionManual(eventos_persistentes)
    return jsonify(result)

@app.route('/modificar_datos_evento', methods=['POST'])
def modificar_datos_evento():
    resultado = gestor.tomarOpcionModificacionDatos(request, lista_alcances, eventos_persistentes, lista_origenes)
    
    if isinstance(resultado, dict) and not resultado.get('success', True):
        status_code = resultado.pop('status_code', 500)
        return jsonify(resultado), status_code
    
    return jsonify(resultado)

@app.route('/ejecutar_accion', methods=['POST'])
def ejecutar_accion():
    data = request.get_json()
    resultado = gestor.tomarSeleccionOpcionEvento(data, estados)
    
    if isinstance(resultado, dict) and not resultado.get('success', True):
        status_code = resultado.pop('status_code', 500)
        return jsonify(resultado), status_code
    
    return jsonify(resultado)

@app.route('/mapa', methods=['GET'])
def mapa():
    msj = gestor.tomarSeleccionDeOpcionMapa()
    return jsonify(msj)

@app.route('/')
def index():
    return send_from_directory('../FRONTEND', 'index.html')

@app.route('/<path:filename>')
def serve_html(filename):
    if filename.endswith('.html'):
        return send_from_directory('../FRONTEND', filename)
    return '', 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
