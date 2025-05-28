document.addEventListener('DOMContentLoaded', function() {
    console.log('Cargando datos del evento...'); // Debug

    // Obtener datos del evento
    fetch('/obtener_datos_evento')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Llenar selects de alcance y origen
                llenarSelect('inputAlcance', data.alcances_sismo, data.evento.alcanceSismo);
                llenarSelect('inputOrigen', data.origenes_generacion, data.evento.origenGeneracion);
                mostrarDatosEvento(data.evento, data.series_temporales);
            } else {
                mostrarError(data.error || 'Error desconocido');
            }
        })
        .catch(error => {
            mostrarError('Error al cargar los datos del evento: ' + error.message);
        });

    // Botones de opciones
    document.getElementById('btnMapa').addEventListener('click', function() {
        alert('Funcionalidad de mapa: aquí se mostraría el evento y las estaciones en un mapa.');
    });

    document.getElementById('btnModificar').addEventListener('click', function() {
        if (!confirm('¿Desea modificar los datos del evento?')) {
            return;
        }
    });

    document.getElementById('btnEjecutarAccion').addEventListener('click', function() {
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
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                alert('Acción ejecutada con éxito');
                window.location.href = '/opciones';
            } else {
                alert(data.error || 'Error al ejecutar la acción');
            }
        });
    });
});

function llenarSelect(id, opciones, valorActual) {
    const select = document.getElementById(id);
    if (!select) return;
    select.innerHTML = '';
    opciones.forEach(op => {
        const opt = document.createElement('option');
        opt.value = op;
        opt.textContent = op;
        if (op === valorActual) opt.selected = true;
        select.appendChild(opt);
    });
}

// Guardar el evento y series actuales en variables globales para actualización local
window.eventoActual = null;
window.seriesTemporalesActuales = null;

function mostrarDatosEvento(evento, seriesTemporales) {
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
    if (window.ultimosAlcances && window.ultimosOrigenes) {
        llenarSelect('inputAlcance', window.ultimosAlcances, evento.alcanceSismo);
        llenarSelect('inputOrigen', window.ultimosOrigenes, evento.origenGeneracion);
    }

    // Mostrar series temporales y muestras
    mostrarSeriesTemporales(seriesTemporales);
}

function mostrarSeriesTemporales(series) {
    const contenedor = document.getElementById('seriesTemporales');
    if (!series || series.length === 0) {
        contenedor.innerHTML = '<div class="alert alert-info">No hay series temporales registradas.</div>';
        return;
    }
    let html = '';
    series.forEach((serie, idx) => {
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

// Modificar datos del evento
(function() {
    const formModificar = document.getElementById('formModificarDatos');
    if (formModificar) {
        formModificar.addEventListener('submit', function(e) {
            e.preventDefault();
            const valorMagnitud = document.getElementById('inputMagnitud').value;
            const alcanceSismo = document.getElementById('inputAlcance').value;
            const origenGeneracion = document.getElementById('inputOrigen').value;
            fetch('/modificar_datos_evento', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ valorMagnitud, alcanceSismo, origenGeneracion })
            })
            .then(r => r.json())
            .then(data => {
                const msg = document.getElementById('mensajeModificacion');
                if (data.success) {
                    msg.textContent = 'Datos modificados correctamente';
                    msg.classList.remove('d-none');
                    msg.classList.remove('alert-danger');
                    msg.classList.add('alert-success');
                    // Actualizar los datos mostrados en pantalla sin recargar
                    if (window.eventoActual) {
                        window.eventoActual.valorMagnitud = valorMagnitud;
                        window.eventoActual.alcanceSismo = alcanceSismo;
                        window.eventoActual.origenGeneracion = origenGeneracion;
                        mostrarDatosEvento(window.eventoActual, window.seriesTemporalesActuales || []);
                    }
                } else {
                    msg.textContent = data.error || 'Error al modificar';
                    msg.classList.remove('d-none');
                    msg.classList.remove('alert-success');
                    msg.classList.add('alert-danger');
                }
            });
        });
    }
})();

function mostrarError(mensaje) {
    const datosPrincipales = document.getElementById('datosPrincipales');
    datosPrincipales.innerHTML = `
        <div class="alert alert-danger">
            ${mensaje}
        </div>
    `;
}

// Al recibir los datos del backend, guardar los valores de los selects para reutilizarlos
fetch('/obtener_datos_evento')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.ultimosAlcances = data.alcances_sismo;
            window.ultimosOrigenes = data.origenes_generacion;
        }
    });