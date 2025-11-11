const API_BASE = 'http://127.0.0.1:5001';

// Helper to show a colored modal with icon and optional redirect
function showResultModal(type, title, message, autoRedirect = false, redirectDelay = 3000) {
    const modalEl = document.getElementById('resultModal');
    if (!modalEl) {
        alert(message);
        if (autoRedirect) setTimeout(() => { window.location.href = 'index.html'; }, redirectDelay);
        return;
    }
    const header = document.getElementById('resultModalHeader');
    const icon = document.getElementById('resultModalIcon');
    const titleEl = document.getElementById('resultModalTitle');
    const textEl = document.getElementById('resultModalText');

    // Reset header classes
    if (header) {
        header.className = 'modal-header';
    }
    // choose appearance
    const appearance = {
        success: { headerClass: 'modal-header bg-success text-white', icon: 'bi-check-circle' , title: title || 'Éxito' },
        danger: { headerClass: 'modal-header bg-danger text-white', icon: 'bi-x-circle', title: title || 'Error' },
        warning: { headerClass: 'modal-header bg-warning text-dark', icon: 'bi-exclamation-triangle', title: title || 'Atención' },
        info: { headerClass: 'modal-header bg-info text-white', icon: 'bi-info-circle', title: title || 'Información' }
    };

    const ap = appearance[type] || appearance.info;
    if (header) header.className = ap.headerClass;
    if (icon) {
        icon.className = `bi ${ap.icon} fs-3 me-2`;
    }
    if (titleEl) titleEl.textContent = ap.title;
    if (textEl) textEl.textContent = message;

    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    // Ensure redirect happens even if modal.show() throws for any reason
    if (autoRedirect) {
        setTimeout(() => { try { window.location.href = 'index.html'; } catch(_) { /* ignore */ } }, redirectDelay);
    }
    try {
        modal.show();
    } catch (e) {
        // If showing modal fails, fallback to alert and rely on timer-based redirect (if enabled)
        if (!autoRedirect) alert(message);
    }
}

// Inline message helper used across the frontend
function showInlineMessage(containerId, text, type = 'info', autoHide = true, timeout = 4000) {
    try {
        const el = document.getElementById(containerId);
        if (!el) {
            // fallback to alert
            alert(text);
            return;
        }
        // normalize classes
        el.classList.remove('d-none', 'alert-success', 'alert-danger', 'alert-info', 'alert-warning');
        const map = {
            success: 'alert-success',
            danger: 'alert-danger',
            error: 'alert-danger',
            warning: 'alert-warning',
            info: 'alert-info'
        };
        const cls = map[type] || 'alert-info';
        el.classList.add('alert', cls);
        el.textContent = text;
        // inline messages are shown visually; no screen-reader live region

        if (autoHide) {
            setTimeout(() => {
                try {
                    el.classList.add('d-none');
                } catch (e) { /* ignore */ }
            }, timeout);
        }
    } catch (e) {
        console.error('showInlineMessage error', e);
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

    // Accessibility & loading helpers
    showLoading(message) {
        try {
            const overlay = document.getElementById('loadingOverlay');
            if (overlay) {
                overlay.classList.remove('d-none');
            }
        } catch (e) {
            // swallow
        }
    }

    hideLoading(message) {
        try {
            const overlay = document.getElementById('loadingOverlay');
            if (overlay) {
                overlay.classList.add('d-none');
            }
        } catch (e) {
            // swallow
        }
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
            // show loading and disable controls
            this.showLoading('Cargando eventos sísmicos...');
            if (select) select.disabled = true;
            const btnReg = document.getElementById('btnRegistrar');
            if (btnReg) btnReg.disabled = true;

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
        } finally {
            // hide loading and re-enable
            this.hideLoading();
            if (select) select.disabled = false;
            const btnReg = document.getElementById('btnRegistrar');
            if (btnReg) btnReg.disabled = false;
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

        // Use async/await with loading state
        (async () => {
            try {
                this.showLoading('Seleccionando evento...');
                const btnReg = document.getElementById('btnRegistrar');
                if (btnReg) btnReg.disabled = true;

                const resp = await fetch(`${API_BASE}/eventos`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datos)
                });
                const data = await resp.json();
                if (data.success) {
                    sessionStorage.setItem('eventoSeleccionado', JSON.stringify(data.evento));
                    sessionStorage.setItem('seriesTemporales', JSON.stringify(data.series_temporales || []));
                    sessionStorage.setItem('ultimosAlcances', JSON.stringify(data.alcances_sismo || []));
                    sessionStorage.setItem('ultimosOrigenes', JSON.stringify(data.origenes_generacion || []));
                    window.location.href = 'datos_evento.html';
                } else {
                    alert(data.error || 'No se pudo seleccionar el evento');
                }
            } catch (error) {
                console.error('Error en fetch:', error);
                alert('Error de conexión con el servidor');
            } finally {
                this.hideLoading();
                const btnReg = document.getElementById('btnRegistrar');
                if (btnReg) btnReg.disabled = false;
            }
        })();
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
        // Indicador (badge) eliminado; feedback se muestra mediante el modal de resultados.
        const btnConfirmar = document.getElementById('btnConfirmar');
        const btnDerivar = document.getElementById('btnDerivar');
        const btnRechazar = document.getElementById('btnRechazar');
        try {
            // UI optimista: deshabilitar botones para evitar envíos dobles
            if (btnConfirmar) btnConfirmar.disabled = true;
            if (btnDerivar) btnDerivar.disabled = true;
            if (btnRechazar) btnRechazar.disabled = true;

            // show loading overlay
            this.showLoading('Ejecutando acción...');

            const body = { accion };

            const response = await fetch(`${API_BASE}/ejecutar_accion`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            let data = null;
            try {
                data = await response.json();
            } catch (parseErr) {
                // parsing error
                // try to read text for debugging
                try {
                    const text = await response.text();
                    // swallow
                } catch (tErr) {
                    // swallow
                }
            }
            if (data && data.success) {
                const msg = data.mensaje || 'Acción ejecutada con éxito';
                // limpiar selección local para evitar doble envío
                sessionStorage.removeItem('eventoSeleccionado');
                sessionStorage.removeItem('seriesTemporales');
                sessionStorage.removeItem('ultimosAlcances');
                sessionStorage.removeItem('ultimosOrigenes');
                // Mostrar modal success y redirigir automáticamente a home
                showResultModal('success', 'Operación exitosa', msg, true, 3000);
            } else {
                const err = data && data.error ? data.error : 'Error al ejecutar la acción';
                showResultModal('danger', 'Error', err, false);
            }
        } catch (error) {
            showResultModal('danger', 'Error de conexión', 'Error de conexión con el servidor', false);
        }
        finally {
            // hide loading and ensure UI re-enabled if modal doesn't redirect
            this.hideLoading();
            if (btnConfirmar) btnConfirmar.disabled = false;
            if (btnDerivar) btnDerivar.disabled = false;
            if (btnRechazar) btnRechazar.disabled = false;
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
        try {
            this.showLoading('Cargando mapa...');
            const response = await fetch(`${API_BASE}/mapa`)
            const data = await response.json();
            alert(data);
        } catch (e) {
            console.error('Error cargando mapa', e);
            alert('Error cargando mapa');
        } finally {
            this.hideLoading();
        }
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
        try {
            this.showLoading('Guardando cambios...');
            const btn = document.getElementById('btnModificar');
            if (btn) btn.disabled = true;

            const r = await fetch(`${API_BASE}/modificar_datos_evento`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ magnitud, alcanceSismo, origenGeneracion })
            });
            const data = await r.json();
            const msg = document.getElementById('mensajeModificacion');
            if (data.success) {
                showInlineMessage('mensajeModificacion', '✓ Datos modificados correctamente', 'success', true, 5000);
                if (window.eventoActual) {
                    const numVal = parseFloat(magnitud) || null;
                    if (window.eventoActual.magnitud) {
                        window.eventoActual.magnitud.numero = numVal;
                    } else {
                        window.eventoActual.magnitud = { numero: numVal, descripcion: null };
                    }
                    window.eventoActual.alcanceSismo = alcanceSismo;
                    window.eventoActual.origenGeneracion = origenGeneracion;
                    sessionStorage.setItem('eventoSeleccionado', JSON.stringify(window.eventoActual));
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
                msg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        } catch (e) {
            console.error('Error modificando datos:', e);
            const msg = document.getElementById('mensajeModificacion');
            if (msg) {
                msg.textContent = '✗ Error de conexión';
                msg.classList.remove('d-none');
                msg.classList.remove('alert-success');
                msg.classList.add('alert-danger');
            }
        } finally {
            this.hideLoading();
            const btn = document.getElementById('btnModificar');
            if (btn) btn.disabled = false;
        }
    }
}

export { PantallaRevisionManual };





