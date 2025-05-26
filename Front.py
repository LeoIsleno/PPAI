from flask import Flask, render_template, url_for, jsonify, request, session
from ListaEventosSismicos import crear_eventos_sismicos
from Modelos.gestores import GestorRevisionManual

# Crear la aplicación Flask
app = Flask(__name__, template_folder='templates', static_folder='static')

# Crear el gestor que maneja la lógica de negocio
gestor = GestorRevisionManual()

# Variable global para almacenar eventos en memoria
eventos_cache = None


# Ruta principal - Muestra la página de login
@app.route('/')
def inicio():
    return render_template('main.html')


# Ruta del menú principal
@app.route('/opciones')
def menu_principal():
    return render_template('opciones.html')


# Ruta para mostrar la lista de eventos sísmicos
@app.route('/registrarRevision')
def mostrar_eventos():
    """Muestra la lista de eventos que pueden ser revisados"""
    try:
        global eventos_cache
        if eventos_cache is None:
            eventos_cache = crear_eventos_sismicos()

        eventos_para_mostrar = []
        for evento in eventos_cache:
            if evento.estaAutoDetectado():
                eventos_para_mostrar.append({
                    'id': id(evento),
                    'fechaHoraOcurrencia': evento.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S'),
                    'latitudEpicentro': evento.getLatitudEpicentro(),
                    'longitudEpicentro': evento.getLongitudEpicentro(),
                    'latitudHipocentro': evento.getLatitudHipocentro(),
                    'longitudHipocentro': evento.getLongitudHipocentro(),
                    'valorMagnitud': evento.getValorMagnitud(),
                    'estado': evento.getEstadoActual().getNombreEstado()
                })

        return render_template('registrar.html', eventos=eventos_para_mostrar)
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('registrar.html', error=str(e))


# Ruta para seleccionar un evento
@app.route('/seleccionar_evento', methods=['POST'])
def seleccionar_evento():
    """Maneja la selección de un evento sísmico"""
    try:
        global eventos_cache
        # Verificar si necesitamos inicializar la caché
        if eventos_cache is None:
            print("Inicializando caché de eventos...")
            eventos_cache = crear_eventos_sismicos()

        # Obtener ID del evento seleccionado
        evento_id = request.json.get('evento_id')
        print(f"Seleccionando evento ID: {evento_id}")

        if not eventos_cache:
            return jsonify({
                'success': False,
                'error': 'No hay eventos disponibles'
            }), 500

        # Buscar el evento en la caché
        evento_seleccionado = next(
            (evento for evento in eventos_cache if id(evento) == evento_id),
            None
        )

        if evento_seleccionado:
            # Bloquear el evento para revisión
            estado_bloqueado = gestor.buscarEstadoBloqueadoEnRevision()

            # Intentar bloquear el evento
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


# Ruta para mostrar los datos del evento seleccionado
@app.route('/mostrar_datos_evento')
def mostrar_datos_evento():
    return render_template('datos_evento.html')


# Ruta para obtener los datos del evento seleccionado
@app.route('/obtener_datos_evento')
def obtener_datos_evento():
    """Obtiene y devuelve los datos del evento seleccionado"""
    try:
        # Obtener el evento seleccionado del gestor
        evento_seleccionado = gestor.obtenerEventoSeleccionado()
        print("Evento seleccionado:", evento_seleccionado)  # Debug

        if not evento_seleccionado:
            print("No hay evento seleccionado")  # Debug
            return jsonify({'success': False, 'error': 'No hay evento seleccionado'}), 404

        # Obtener los datos del evento
        datos_sismicos = gestor.buscarDatosSismicos(evento_seleccionado)
        print("Datos sísmicos:", datos_sismicos)  # Debug

        return jsonify({
            'success': True,
            'evento': datos_sismicos
        })
    except Exception as e:
        print(f"Error obteniendo datos del evento: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/ejecutar_accion', methods=['POST'])
def ejecutar_accion():
    try:
        accion = request.json.get('accion')
        evento = gestor.obtenerEventoSeleccionado()

        if not evento:
            return jsonify({
                'success': False,
                'error': 'No hay evento seleccionado'
            }), 404

        if accion == 'rechazar':
            if gestor.validarDatosMinimosRequeridos(evento):
                gestor.rechazarEventoSismico(evento)
                return jsonify({'success': True})
            else:
                return jsonify({
                    'success': False,
                    'error': 'Faltan datos mínimos requeridos'
                }), 400

        return jsonify({'success': False, 'error': 'Acción no válida'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
