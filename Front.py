# Front.py - Aplicación principal Flask para la gestión de eventos sísmicos
# Este archivo define las rutas y la lógica principal del backend de la aplicación.

from flask import Flask, render_template, url_for, jsonify, request, session
from ListaEventosSismicos import crear_eventos_sismicos
from Modelos.evento_sismico import EventoSismico
from Modelos.gestores import GestorRevisionManual

# Crear la aplicación Flask, especificando las carpetas de plantillas y archivos estáticos
app = Flask(__name__, template_folder='templates', static_folder='static')

# Instanciar el gestor que maneja la lógica de negocio relacionada a la revisión manual de eventos
# Este objeto centraliza la lógica de obtención, bloqueo y modificación de eventos
gestor = GestorRevisionManual()

# Variable global para almacenar en memoria los eventos sísmicos generados
# Esto evita recrear los eventos en cada request
# (En una app real, esto sería una base de datos)
eventos_cache = None

# ---------------------- RUTAS PRINCIPALES ----------------------

# Ruta principal - Muestra la página de login
@app.route('/')
def inicio():
    return render_template('main.html')

# Ruta del menú principal
@app.route('/opciones')
def menu_principal():
    return render_template('opciones.html')

# Ruta para mostrar la lista de eventos sísmicos disponibles para revisión
@app.route('/registrarRevision')
def mostrar_eventos():
    """Muestra la lista de eventos que pueden ser revisados (solo los auto-detectados)"""
    try:
        global eventos_cache
        # Si la caché está vacía, crear los eventos sísmicos de ejemplo
        if eventos_cache is None:
            eventos_cache, alcances_sismo, origenes_generacion = crear_eventos_sismicos()
        else:
            # Si ya existe la caché, obtener los valores de los desplegables de la función
            _, alcances_sismo, origenes_generacion = crear_eventos_sismicos()

        eventos_para_mostrar = []
        # Filtrar solo los eventos auto-detectados y armar la estructura para la vista
        for evento in eventos_cache:
            if evento.estaAutoDetectado():
                eventos_para_mostrar.append({
                    'id': evento.id_evento,  # Usar el identificador único persistente
                    'fechaHoraOcurrencia': evento.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S'),
                    'latitudEpicentro': evento.getLatitudEpicentro(),
                    'longitudEpicentro': evento.getLongitudEpicentro(),
                    'latitudHipocentro': evento.getLatitudHipocentro(),
                    'longitudHipocentro': evento.getLongitudHipocentro(),
                    'valorMagnitud': evento.getValorMagnitud(),
                    'estado': evento.getEstadoActual().getNombreEstado()
                })

        # Renderizar la plantilla con la lista de eventos y los valores de los desplegables
        return render_template('registrar.html', eventos=eventos_para_mostrar, alcances_sismo=alcances_sismo, origenes_generacion=origenes_generacion)
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('registrar.html', error=str(e))

# ---------------------- SELECCIÓN Y BLOQUEO DE EVENTO ----------------------

# Ruta para seleccionar un evento y bloquearlo para revisión
@app.route('/seleccionar_evento', methods=['POST'])
def seleccionar_evento():
    """Maneja la selección de un evento sísmico y lo bloquea para revisión"""
    try:
        global eventos_cache
        # Inicializar la caché si es necesario
        if eventos_cache is None:
            print("Inicializando caché de eventos...")
            eventos_cache = crear_eventos_sismicos()

        # Obtener el ID del evento seleccionado desde el frontend
        evento_id = request.json.get('evento_id')
        print(f"Seleccionando evento ID: {evento_id}")

        if not eventos_cache:
            return jsonify({
                'success': False,
                'error': 'No hay eventos disponibles'
            }), 500

        # Buscar el evento en la caché por su id persistente
        evento_seleccionado = next(
            (evento for evento in eventos_cache if evento.id_evento == evento_id),
            None
        )

        if evento_seleccionado:
            # Buscar el estado 'BloqueadoEnRevision' para bloquear el evento
            estado_bloqueado = gestor.buscarEstadoBloqueadoEnRevision()
            
            if not estado_bloqueado:
                return jsonify({
                    'success': False,
                    'error': 'Error al crear el estado bloqueado'
                }), 500

            # Intentar bloquear el evento (cambiar su estado)
            if gestor.bloquearEventoSismico(evento_seleccionado, estado_bloqueado):
                print(f"Evento bloqueado exitosamente. ID: {evento_id}")
                return jsonify({
                    'success': True,
                    'redirect': url_for('mostrar_datos_evento')
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'No se pudo bloquear el evento'
                }), 400
        else:
            return jsonify({
                'success': False,
                'error': f'No se encontró el evento con ID: {evento_id}'
            }), 404

    except Exception as e:
        print(f"Error en seleccionar_evento: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error del servidor: {str(e)}'
        }), 500

# ---------------------- VISUALIZACIÓN Y MODIFICACIÓN DE DATOS DEL EVENTO ----------------------

# Ruta para mostrar la página de datos del evento seleccionado
@app.route('/mostrar_datos_evento')
def mostrar_datos_evento():
    return render_template('datos_evento.html')

# Ruta para obtener los datos completos del evento seleccionado (incluye series temporales y muestras)
@app.route('/obtener_datos_evento')
def obtener_datos_evento():
    """Obtiene y devuelve los datos del evento seleccionado usando obtenerSeriesTemporales, que inicia el recorrido de getDatos"""
    try:
        evento = gestor.obtenerEventoSeleccionado()
        if not evento:
            return jsonify({'success': False, 'error': 'No hay evento seleccionado'}), 404

        # Obtener valores de los desplegables
        _, alcances_sismo, origenes_generacion = crear_eventos_sismicos()

        # Datos principales del evento (sin series)
        alcance = evento.getAlcanceSismo()
        clasificacion = evento.getClasificacion()
        origen = evento.getOrigenGeneracion()
        datos_evento = {
            'alcanceSismo': alcance.getNombre() if alcance else 'No disponible',
            'clasificacion': clasificacion.getNombre() if clasificacion else 'No disponible',
            'origenGeneracion': origen.getNombre() if origen else 'No disponible',
            'descripcionAlcance': alcance.getDescripcion() if alcance else 'No disponible',
            'valorMagnitud': str(evento.getValorMagnitud()),
            'fechaHoraOcurrencia': evento.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S') if evento.getFechaHoraOcurrencia() else 'No disponible',
            'latitudEpicentro': str(evento.getLatitudEpicentro()) if evento.getLatitudEpicentro() is not None else 'No disponible',
            'longitudEpicentro': str(evento.getLongitudEpicentro()) if evento.getLongitudEpicentro() is not None else 'No disponible',
            'latitudHipocentro': str(evento.getLatitudHipocentro()) if evento.getLatitudHipocentro() is not None else 'No disponible',
            'longitudHipocentro': str(evento.getLongitudHipocentro()) if evento.getLongitudHipocentro() is not None else 'No disponible'
        }

        # Usar el método del gestor para obtener las series temporales y que este inicie el recorrido de getDatos
        series_temporales = gestor.obtenerSeriesTemporales(evento)
        gestor.llamarCUGenerarSismograma(evento)

        return jsonify({
            'success': True,
            'evento': datos_evento,
            'series_temporales': series_temporales,
            'alcances_sismo': alcances_sismo,
            'origenes_generacion': origenes_generacion
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Ruta para modificar los datos principales del evento seleccionado
@app.route('/modificar_datos_evento', methods=['POST'])
def modificar_datos_evento():
    """Permite modificar magnitud, alcance y origen de generación del evento seleccionado"""
    try:
        evento = gestor.obtenerEventoSeleccionado()
        if not evento:
            return jsonify({'success': False, 'error': 'No hay evento seleccionado'}), 404
        data = request.json
        if 'valorMagnitud' in data:
            evento.setValorMagnitud(data['valorMagnitud'])
        if 'alcanceSismo' in data:
            evento.setAlcanceSismo(data['alcanceSismo'])
        if 'origenGeneracion' in data:
            evento.setOrigenGeneracion(data['origenGeneracion'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ---------------------- ACCIONES SOBRE EL EVENTO (EJ: RECHAZAR) ----------------------

# Ruta para ejecutar acciones sobre el evento seleccionado (ejemplo: rechazar)
@app.route('/ejecutar_accion', methods=['POST'])
def ejecutar_accion():
    try:
        accion = request.json.get('accion')
        evento = gestor.obtenerEventoSeleccionado()
        usuario = session.get('usuario', 'desconocido')  # Simulación de usuario logueado
        if not evento:
            return jsonify({
                'success': False,
                'error': 'No hay evento seleccionado'
            }), 404
        if accion == 'rechazar':
            # Validar que el evento tenga los datos mínimos requeridos antes de rechazar
            if gestor.validarDatosMinimosRequeridos(evento):
                gestor.rechazarEventoSismico(evento, usuario)
                return jsonify({'success': True})
            else:
                return jsonify({
                    'success': False,
                    'error': 'Faltan datos mínimos requeridos'
                }), 400
        return jsonify({'success': False, 'error': 'Acción no válida'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ---------------------- INICIO DE LA APLICACIÓN ----------------------

if __name__ == '__main__':
    # Ejecutar la aplicación Flask en modo debug
    app.run(host='0.0.0.0', port=5001, debug=True)
