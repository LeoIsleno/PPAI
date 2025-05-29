class PantallaRevisionManual {

    constructor(cboEventoSismicos) {
        this.cboEventoSismicos = cboEventoSismicos;
    }

    async OpRegistrarResultadoRevisionManual() {
        window.location.href = '/registrarRevision';
    }

    async mostrarEventosSismicos() {
        const select = document.getElementById('evento');
        const mensaje = document.getElementById('mensajeEventos');

        try {
            const response = await fetch('/api/eventos');
            const eventos = await response.json();

            select.innerHTML = `<option value="" disabled selected>Seleccione un evento sísmico...</option>`;

            if (eventos.length === 0) {
                mensaje.textContent = 'No hay eventos sísmicos disponibles.';
                mensaje.classList.remove('d-none');
            } else {
                mensaje.classList.add('d-none');
                eventos.forEach(evento => {
                    const texto = `${evento[0]} | Magnitud: ${evento[5]} | Epicentro: (${evento[1]}, ${evento[2]}) | Hipocentro: (${evento[3]}, ${evento[4]})`;
                    const option = document.createElement('option');
                    option.value = JSON.stringify(evento);
                    option.textContent = texto;
                    select.appendChild(option);
                });
            }
            // Guarda la referencia al select en la instancia
            this.cboEventoSismicos = select;
        } catch (error) {
            mensaje.textContent = 'Error al cargar los eventos sísmicos.';
            mensaje.classList.remove('d-none');
        }
    }

    solicitarEventoSismico() {
        const evento = document.getElementById("evento");
        this.cboEventoSismicos = evento;
    }

    tomarSeleccionEventoSismico() {
        const valor = this.cboEventoSismicos.value;
        if (!valor) {
            alert('Debe seleccionar un evento');
            return;
        }
        const evento = JSON.parse(valor);

        const datos = {
            magnitud: evento[5],
            latEpicentro: evento[1],
            longEpicentro: evento[2],
            latHipocentro: evento[3],
            longHipocentro: evento[4]
        };

        fetch('/eventos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.redirect) {
                window.location.href = data.redirect;
            } else {
                alert(data.error || 'No se pudo seleccionar el evento');
            }
        })
        .catch(error => {
            console.error('Error al solicitar evento sísmico:', error);
        });
    }

    mostrarDatosSismicos() {
        datos_series = EventoSismico.obtenerSeriesTemporales();

        datos_sismicoos = EventoSismico.obtenerDatosSismicos();

        return jsonify({
            'success': True,
            'evento': datos_sismicoos,
            'series_temporales': datos_series,
            'alcances_sismo': alcances_sismo,
            'origenes_generacion': origenes_generacion
        })
    }

    tomarSeleccionOpcionEvento() {
        const accion = document.getElementById('accionEvento').value;
        if (!accion) {
            alert('Por favor seleccione una acción');
            return;
        }

        fetch('/ejecutar_accion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ accion })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.mensaje || 'Acción ejecutada con éxito');
                window.location.href = '/'; // Redirigir al índice después de la acción
            } else {
                alert(data.error || 'Error al ejecutar la acción');
            }
        });
    }




}


export { PantallaRevisionManual };





