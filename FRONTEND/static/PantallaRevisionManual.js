const API_BASE = 'http://127.0.0.1:5001';

class PantallaRevisionManual {

    constructor(cboEventoSismicos, btnAccion) {
        this.cboEventoSismicos = cboEventoSismicos;
        this.btnAccion = btnAccion;
    }

    async opRegistrarResultadoRevisionManual() {
        window.location.href = 'registrar.html';
    }

    async mostrarEventosSismicos() {
        const select = document.getElementById('evento');
        const mensaje = document.getElementById('mensajeEventos');

        try {
            const response = await fetch(`${API_BASE}/api/eventos`);
            const eventos = await response.json();

            select.innerHTML = '';
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.selected = true;
            defaultOption.textContent = 'Seleccione un evento sísmico...';
            select.appendChild(defaultOption);

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
        // if (!valor) return;
        // const evento = JSON.parse(valor);

        // const datos = {
        //     magnitud: evento[5],
        //     latEpicentro: evento[1],
        //     longEpicentro: evento[2],
        //     latHipocentro: evento[3],
        //     longHipocentro: evento[4]
        // };

        // fetch(`${API_BASE}/eventos`, {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(datos)
        // })
        // .then(response => response.json())
        // .then(data => {
        //     if (data.success) {
        //         fetch(`${API_BASE}/obtener_datos_evento`)
        //             .then(response => response.json())
        //             .then(data => {
        //                 if (data.success) {
        //                     // Aquí puedes manejar los datos recibidos si es necesario
        //                 }
        //             });
        //     }
        // });
        } catch (error) {
            mensaje.textContent = 'Error al cargar los eventos sísmicos.';
            mensaje.classList.remove('d-none');
        }
    }


    solicitarEventoSismico() {
        const evento = document.getElementById("evento");
        this.cboEventoSismicos = evento;
    }

    
    tomarSeleccionDeEventoSismico() {
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

        console.log('[DEBUG] Enviando datos al backend:', datos);

        fetch(`${API_BASE}/eventos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                sessionStorage.setItem('eventoSeleccionado', JSON.stringify(data.evento));
                sessionStorage.setItem('seriesTemporales', JSON.stringify(data.series_temporales || []));
                sessionStorage.setItem('ultimosAlcances', JSON.stringify(data.alcances_sismo || []));
                sessionStorage.setItem('ultimosOrigenes', JSON.stringify(data.origenes_generacion || []));
                window.location.href = 'datos_evento.html'; // Redirigir a la página de datos del evento
            } else {
                alert(data.error || 'No se pudo seleccionar el evento');
                console.warn('[WARN] No se pudo seleccionar el evento:', data);
            }
        });
    }

    mostrarDatosSismicos(evento, seriesTemporales, alcance, origenSismico) {
        window.eventoActual = evento;
        window.seriesTemporalesActuales = seriesTemporales;
        const datosPrincipales = document.getElementById('datosPrincipales');
        if (!evento) {
            mostrarError('No se pudieron cargar los datos del evento');
            return;
        }
        datosPrincipales.innerHTML = `
            <div class="card mb-3">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Información del Evento</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h6 class="text-muted mb-3">Clasificación y Alcance</h6>
                            <p><strong>Clasificación:</strong> ${evento.clasificacion || 'No disponible'}</p>
                            <p><strong>Alcance:</strong> ${evento.alcanceSismo || 'No disponible'}</p>
                            <p><strong>Descripción:</strong> ${evento.descripcionAlcance || 'No disponible'}</p>
                            <p><strong>Origen:</strong> ${evento.origenGeneracion || 'No disponible'}</p>
                        </div>
                        <div class="col-md-6">
                            <h6 class="text-muted mb-3">Datos Técnicos</h6>
                            <p><strong>Magnitud:</strong> ${evento.valorMagnitud || 'No disponible'}</p>
                            <p><strong>Fecha/Hora:</strong> ${evento.fechaHoraOcurrencia || 'No disponible'}</p>
                            <p><strong>Epicentro:</strong> (${evento.latitudEpicentro || '?'}, ${evento.longitudEpicentro || '?'})</p>
                            <p><strong>Hipocentro:</strong> (${evento.latitudHipocentro || '?'}, ${evento.longitudHipocentro || '?'})</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        // Llenar los inputs del formulario de modificación
        document.getElementById('inputMagnitud').value = evento.valorMagnitud || '';
        // Llenar selects de alcance y origen con el valor actual
        if (alcance && origenSismico) {
            window.ultimosAlcances = alcance;
            window.ultimosOrigenes = origenSismico;
            const select = document.getElementById('inputAlcance');
            if (!select) return;
            select.innerHTML = '';
            window.ultimosAlcances.forEach(op => {
                const opt = document.createElement('option');
                opt.value = op;
                opt.textContent = op;
                if (op === evento.alcanceSismo) opt.selected = true;
                select.appendChild(opt);
            });

            const origen = document.getElementById('inputOrigen');
            if (!origen) return;
            origen.innerHTML = '';
            window.ultimosOrigenes.forEach(op => {
                const opt = document.createElement('option');
                opt.value = op;
                opt.textContent = op;
                if (op === evento.origenGeneracion) opt.selected = true;
                origen.appendChild(opt);
            });
        }

        // Mostrar series temporales y muestras
        const contenedor = document.getElementById('seriesTemporales');
        if (!seriesTemporales || seriesTemporales.length === 0) {
            contenedor.innerHTML = '<div class="alert alert-info">No hay series temporales registradas.</div>';
            return;
        }
        let html = '';
        seriesTemporales.forEach((serie, idx) => {
            html += `<div class="card mb-2">
                <div class="card-header bg-light">
                    <strong>Serie temporal #${idx + 1}</strong><br>
                    <span><b>Fecha/Hora inicio:</b> ${serie.fechaHoraInicioRegistroMuestras}</span><br>
                    <span><b>Frecuencia de muestreo:</b> ${serie.frecuenciaMuestreo} Hz</span><br>
                    <span><b>Alerta de alarma:</b> ${serie.condicionAlarma}</span>
                </div>
                <div class="card-body">
                    <h6 class="mb-2">Muestras sísmicas:</h6>
                    <ul class="list-group">`;
            serie.muestras.forEach((muestra, j) => {
                html += `<li class="list-group-item">
                    <b>Fecha/Hora muestra ${j + 1}:</b> ${muestra.fechaHoraMuestra}<br>
                    <ul style="margin-left: 1em;">`;
                muestra.detalle.forEach(det => {
                    html += `
                        <li style="font-style:italic;">
                            ${det.tipoDeDato === 'Velocidad de onda' ? '<b>Velocidad de onda:</b>' : ''}
                            ${det.tipoDeDato === 'Frecuencia de onda' ? '<b>Frecuencia de onda:</b>' : ''}
                            ${det.tipoDeDato === 'Longitud' ? '<b>Longitud:</b>' : ''}
                            ${det.valor}
                        </li>
                    `;
                });
                html += `
                    </ul>
                </li>`;
            });
            html += `</ul></div></div>`;
        });
        contenedor.innerHTML = html;
    }

    pedirOpcionEveneto() {
        const accion = document.getElementById('accionEvento')
        this.btnAccion = accion;
    }

    tomarSeleccionOpcionEvento() {
        const accion = this.btnAccion.value;
        if (!accion) {
            alert('Por favor seleccione una acción');
            return;
        }
        fetch(`${API_BASE}/ejecutar_accion`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ accion })
        })
        .then(r => r.json())
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





