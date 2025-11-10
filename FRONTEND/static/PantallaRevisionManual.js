const API_BASE = 'http://127.0.0.1:5001';

// Lightweight inline message helper - reverts to previous inline-alert behavior
function showInlineMessage(containerId, text, level = 'info', autoHide = false, timeout = 5000) {
    const el = document.getElementById(containerId);
    if (!el) {
        // fallback to native alert if container not present
        if (level === 'error' || level === 'danger') {
            alert(text);
        } else {
            console.info(text);
        }
        return;
    }
    // normalize level -> bootstrap alert classes
    const levelClass = level === 'success' ? 'alert-success'
                     : (level === 'error' || level === 'danger') ? 'alert-danger'
                     : (level === 'warning') ? 'alert-warning' : 'alert-info';
    el.className = `alert ${levelClass}`; // reset classes
    el.textContent = text;
    el.classList.remove('d-none');
    // optional auto hide
    if (autoHide) {
        setTimeout(() => {
            if (el) el.classList.add('d-none');
        }, timeout);
    }
}

class PantallaRevisionManual {

    constructor(cboEventoSismicos, btnAccion, cboValorMagnitud, cboAlcanceSismo, cboOrigenGeneracion) {
        this.cboEventoSismicos = cboEventoSismicos;
        this.btnAccion = btnAccion;
        this.cboValorMagnitud = cboValorMagnitud;
        this.cboAlcanceSismo = cboAlcanceSismo;
        this.cboOrigenGeneracion = cboOrigenGeneracion;
    }

    // Formatea fecha/hora al estilo local argentino: DD/MM/AAAA HH:MM:SS
    formatDate(fechaIso) {
        try {
            if (!fechaIso) return null;
            const d = new Date(fechaIso);
            if (Number.isNaN(d.getTime())) return fechaIso;
            const pad = (n) => n.toString().padStart(2, '0');
            const day = pad(d.getDate());
            const month = pad(d.getMonth() + 1);
            const year = d.getFullYear();
            const hours = pad(d.getHours());
            const minutes = pad(d.getMinutes());
            const seconds = pad(d.getSeconds());
            return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
        } catch (e) {
            return fechaIso;
        }
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
                    const mag = evento[5] && evento[5].numero ? evento[5].numero : 'No disponible';
                    const texto = `${evento[0]} | Magnitud: ${mag} | Epicentro: (${evento[1]}, ${evento[2]}) | Hipocentro: (${evento[3]}, ${evento[4]})`;
                    const option = document.createElement('option');
                    option.value = JSON.stringify(evento);
                    option.textContent = texto;
                    select.appendChild(option);
                });
            }
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
                window.location.href = 'datos_evento.html';
            } else {
                alert(data.error || 'No se pudo seleccionar el evento');
            }
        })
        .catch(error => {
            console.error('Error en fetch:', error);
            alert('Error de conexión con el servidor');
        });
    }

    mostrarDatosSismicos(evento, seriesTemporales, alcance, origenSismico) {
        window.eventoActual = evento;
        window.seriesTemporalesActuales = seriesTemporales;
        const datosPrincipales = document.getElementById('datosPrincipales');
        if (!evento) {
            const datosPrincipales = document.getElementById('datosPrincipales');
            datosPrincipales.innerHTML = 
                `<div class="alert alert-danger">
                    ${'No se pudieron cargar los datos del evento'}
                </div>`;
            return;
        }
        datosPrincipales.innerHTML = `
            <div class="row g-3">
                <div class="col-md-6">
                    <div class="info-card">
                        <h6 class="info-card-title">
                            <i class="bi bi-diagram-3 me-2"></i>
                            Clasificación y Alcance
                        </h6>
                        <div class="info-item">
                            <i class="bi bi-tag"></i>
                            <div>
                                <strong>Clasificación</strong>
                                <span>${evento.clasificacion || 'No disponible'}</span>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="bi bi-geo-alt"></i>
                            <div>
                                <strong>Alcance</strong>
                                <span>${evento.alcanceSismo || 'No disponible'}</span>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="bi bi-card-text"></i>
                            <div>
                                <strong>Descripción</strong>
                                <span>${evento.descripcionAlcance || 'No disponible'}</span>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="bi bi-lightning"></i>
                            <div>
                                <strong>Origen</strong>
                                <span>${evento.origenGeneracion || 'No disponible'}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-card">
                        <h6 class="info-card-title">
                            <i class="bi bi-clipboard-data me-2"></i>
                            Datos Técnicos
                        </h6>
                        <div class="info-item">
                            <i class="bi bi-speedometer"></i>
                            <div>
                                <strong>Magnitud</strong>
                                <span class="badge-magnitude">${
                                    (evento.magnitud && evento.magnitud.numero) || 'No disponible'
                                }</span>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="bi bi-calendar-event"></i>
                            <div>
                                <strong>Fecha/Hora</strong>
                                <span>${this.formatDate(evento.fechaHoraOcurrencia) || 'No disponible'}</span>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="bi bi-pin-map"></i>
                            <div>
                                <strong>Epicentro</strong>
                                <span>(${evento.latitudEpicentro || '?'}, ${evento.longitudEpicentro || '?'})</span>
                            </div>
                        </div>
                        <div class="info-item">
                            <i class="bi bi-pin-map-fill"></i>
                            <div>
                                <strong>Hipocentro</strong>
                                <span>(${evento.latitudHipocentro || '?'}, ${evento.longitudHipocentro || '?'})</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        // Llenar los inputs del formulario de modificación
    // Preferir el objeto magnitud si existe
    document.getElementById('inputMagnitud').value = (evento.magnitud && evento.magnitud.numero) || '';
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
        const seriesPorEstacion = {};
        seriesTemporales.forEach(serie => {
            const estacion = serie.estacionSismologica || {};
            const nombre = estacion.nombreEstacion || 'Estación Desconocida';
            if (!seriesPorEstacion[nombre]) {
                seriesPorEstacion[nombre] = [];
            }
            seriesPorEstacion[nombre].push(serie);
        });

        Object.entries(seriesPorEstacion).forEach(([nombreEstacion, series]) => {
            const estacion = series[0].estacionSismologica || {};
            const codigo = estacion.codigoEstacion || 'N/A';
            
            html += `<div class="card mb-3 border-0 shadow-sm">
            <div class="card-header" style="background: linear-gradient(135deg, #1a237e 0%, #283593 100%); color: white;">
                <strong><i class="bi bi-geo-fill me-2"></i>${nombreEstacion} (${codigo})</strong>
            </div>
            <div class="card-body">`;

            series.forEach((serie, idx) => {
                html += `
                <div class="mb-4 p-3 border-start border-primary border-3" style="background-color: #f8f9fa;">
                    <div class="d-flex align-items-center mb-2">
                        <i class="bi bi-graph-up text-primary me-2"></i>
                        <strong style="color: var(--primary-dark);">Serie temporal #${idx + 1}</strong>
                    </div>
                    <div class="mb-2">
                        <i class="bi bi-calendar-event me-2 text-muted"></i>
                        <strong>Fecha/Hora inicio:</strong> ${this.formatDate(serie.fechaHoraInicioRegistroMuestras) || 'No disponible'}
                    </div>
                    <div class="mb-3">
                        <i class="bi bi-speedometer2 me-2 text-muted"></i>
                        <strong>Frecuencia de muestreo:</strong> ${serie.frecuenciaMuestreo || 'N/A'} Hz
                    </div>
                    <h6 class="mt-3 mb-2" style="color: var(--primary-dark);">
                        <i class="bi bi-collection me-2"></i>Muestras sísmicas:
                    </h6>
                    <ul class="list-group list-group-flush">`;
            serie.muestras.forEach((muestra, j) => {
                html += `<li class="list-group-item" style="background-color: white;">
                    <div class="d-flex align-items-center mb-2">
                        <i class="bi bi-clock-history me-2" style="color: var(--accent);"></i>
                        <strong>Muestra #${j + 1}:</strong> 
                        <span class="ms-2 text-muted">${this.formatDate(muestra.fechaHoraMuestra) || 'No disponible'}</span>
                    </div>
                    <ul class="ms-4 mb-0">`;
                
                if (muestra.detalle && muestra.detalle.length > 0) {
                    muestra.detalle.forEach(det => {
                        const icono = det.tipoDeDato === 'Velocidad de onda' ? 'speedometer' : 
                                     det.tipoDeDato === 'Frecuencia de onda' ? 'activity' : 'rulers';
                        const unidad = det.unidad ? ` ${det.unidad}` : '';
                        html += `
                        <li class="mb-1">
                            <i class="bi bi-${icono} me-2" style="color: var(--accent);"></i>
                            <strong>${det.tipoDeDato || 'Dato'}:</strong> ${det.valor || 'N/A'}${unidad}
                        </li>`;
                    });
                } else {
                    html += `<li class="text-muted">Sin detalles disponibles</li>`;
                }
                
                html += `
                    </ul>
                </li>`;
            });
            html += `</ul>
                </div>`;
            });

            html += `</div></div>`;
        });
        contenedor.innerHTML = html;
    }

    pedirOpcionEvento() {
        const accion = document.getElementById('accionEvento')
        this.btnAccion = accion;
    }
    tomarSeleccionOpcionEvento() {
        // Mantener compatibilidad con versiones anteriores que usaban un select.
        const accion = this.btnAccion ? this.btnAccion.value : null;
        if (!accion) {
            alert('Por favor seleccione una acción');
            return;
        }
        this.ejecutarAccion(accion);
    }

    async ejecutarAccion(accion) {
        // Ejecuta la acción indicada para el evento actualmente seleccionado.
        // Indicador (badge) eliminado; se muestra únicamente feedback mediante el área de mensajes.
        const mensajeEl = document.getElementById('mensajeAccion');
        const btnConfirmar = document.getElementById('btnConfirmar');
        const btnDerivar = document.getElementById('btnDerivar');
        const btnRechazar = document.getElementById('btnRechazar');
        try {
            console.debug('ejecutarAccion called with', accion);
            // UI optimista: mostrar un mensaje inline mientras se procesa la acción
            showInlineMessage('mensajeAccion', 'Procesando acción...', 'info', false);

            const body = { accion };
            console.debug('ejecutarAccion: enviando fetch', { url: `${API_BASE}/ejecutar_accion`, body });

            const response = await fetch(`${API_BASE}/ejecutar_accion`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            console.debug('ejecutarAccion: fetch completed', { ok: response.ok, status: response.status, statusText: response.statusText });
            let data = null;
            try {
                data = await response.json();
            } catch (parseErr) {
                console.error('ejecutarAccion: error parsing JSON response', parseErr);
                // try to read text for debugging
                try {
                    const text = await response.text();
                    console.error('ejecutarAccion: response text:', text);
                } catch (tErr) {
                    console.error('ejecutarAccion: error reading response text', tErr);
                }
            }
            console.debug('ejecutarAccion response', data);
            if (data && data.success) {
                // Mostrar mensaje en la página y deshabilitar botones de acción
                showInlineMessage('mensajeAccion', data.mensaje || 'Acción ejecutada con éxito', 'success', true, 5000);
                // limpiar selección local para evitar doble envío
                sessionStorage.removeItem('eventoSeleccionado');
                sessionStorage.removeItem('seriesTemporales');
                sessionStorage.removeItem('ultimosAlcances');
                sessionStorage.removeItem('ultimosOrigenes');
                if (btnConfirmar) btnConfirmar.disabled = true;
                if (btnDerivar) btnDerivar.disabled = true;
                if (btnRechazar) btnRechazar.disabled = true;
                // NOTE: previously we redirected to index.html after a short delay.
                // This caused unexpected immediate navigations in some flows. Disable automatic redirect
                // so the user can see the inline message. If you want to re-enable automatic redirect,
                // set `autoRedirectToHome = true` globally.
                try {
                    const autoRedirectToHome = window.autoRedirectToHome || false;
                    if (autoRedirectToHome) {
                        setTimeout(() => {
                            console.debug('Redirecting to index.html after successful action (autoRedirectToHome=true)');
                            window.location.href = 'index.html';
                        }, 5000);
                    } else {
                        console.debug('Automatic redirect suppressed (autoRedirectToHome=false)');
                    }
                } catch (e) {
                    console.error('Error checking autoRedirectToHome flag', e);
                }
            } else {
                showInlineMessage('mensajeAccion', data && data.error ? data.error : 'Error al ejecutar la acción', 'error', true, 6000);
            }
        } catch (error) {
            console.error('Error en ejecutarAccion:', error);
            showInlineMessage('mensajeAccion', 'Error de conexión con el servidor', 'error', true, 6000);
        }
    }

    mostrarOpcionMapa(){
        const contenedor = document.getElementById('opcionMapa');
        if (contenedor) {
            contenedor.innerHTML = `
                <button type="button" id="btnMapa" class="btn btn-accent mb-3">
                    <i class="bi bi-map me-2"></i>
                    Ver Mapa
                </button>`;
        }
    }


    async tomarSeleccionDeOpcionMapa() {

        const response = await fetch(`${API_BASE}/mapa`)
        const data = await response.json();

        alert(data);
    }
    
    pedirOpcionModificarDatos() {
        const inputMagnitud = document.getElementById('inputMagnitud');
        const alcanceSismo = document.getElementById('inputAlcance');
        const origenGeneracion = document.getElementById('inputOrigen');
        this.cboValorMagnitud = inputMagnitud;
        this.cboAlcanceSismo = alcanceSismo;
        this.cboOrigenGeneracion = origenGeneracion;
    }

    async tomarOpcionModificacionDatos() {
        const magnitud = this.cboValorMagnitud.value;
        const alcanceSismo = this.cboAlcanceSismo.value;
        const origenGeneracion = this.cboOrigenGeneracion.value;
        console.debug('tomarOpcionModificacionDatos', { magnitud, alcanceSismo, origenGeneracion });
        await fetch(`${API_BASE}/modificar_datos_evento`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ magnitud, alcanceSismo, origenGeneracion })
        })
        .then(r => r.json())
        .then(data => {
            const msg = document.getElementById('mensajeModificacion');
                if (data.success) {
                // Inline message (reverting notify.js usage)
                showInlineMessage('mensajeModificacion', '✓ Datos modificados correctamente', 'success', true, 5000);
                // Actualizar los datos mostrados en pantalla sin recargar
                if (window.eventoActual) {
                    // Actualizar el objeto magnitud (no usamos el campo legacy valorMagnitud)
                    const numVal = parseFloat(magnitud) || null;
                    if (window.eventoActual.magnitud) {
                        window.eventoActual.magnitud.numero = numVal;
                    } else {
                        window.eventoActual.magnitud = { numero: numVal, descripcion: null };
                    }
                    window.eventoActual.alcanceSismo = alcanceSismo;
                    window.eventoActual.origenGeneracion = origenGeneracion;
                    // Actualizar también en sessionStorage
                    sessionStorage.setItem('eventoSeleccionado', JSON.stringify(window.eventoActual));
                    // Llama al método de la instancia actual para refrescar los datos
                    this.mostrarDatosSismicos(
                        window.eventoActual,
                        window.seriesTemporalesActuales || [],
                        window.ultimosAlcances || [],
                        window.ultimosOrigenes || []
                    );
                }
            } else {
                msg.textContent = '✗ ' + (data.error || 'Error al modificar');
                msg.classList.remove('d-none');
                msg.classList.remove('alert-success');
                msg.classList.add('alert-danger');
                // Hacer scroll al mensaje
                msg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
    }
}

export { PantallaRevisionManual };





