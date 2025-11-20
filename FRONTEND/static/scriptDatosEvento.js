const API_BASE = 'http://127.0.0.1:5001';
import { PantallaRevisionManual } from "./PantallaRevisionManual.js";
const pantalla = new PantallaRevisionManual();

    document.addEventListener('DOMContentLoaded', function() { 
        // Restore persisted console messages (if any) so debug survives a reload.
        try {
            const persisted = sessionStorage.getItem('debugConsoleMessages');
            if (persisted) {
                const arr = JSON.parse(persisted);
                if (Array.isArray(arr)) {
                    arr.forEach(item => {
                        // replay with original level
                        try {
                            if (item && item.level && console[item.level]) {
                                console[item.level].apply(console, item.args || []);
                            } else {
                                console.log.apply(console, item.args || []);
                            }
                        } catch (e) {
                            console.log('Persisted log replay error', e);
                        }
                    });
                }
                sessionStorage.removeItem('debugConsoleMessages');
            }
        } catch (e) {
            console.error('Error restoring persisted console messages', e);
        }
    // DOMContentLoaded
        // Global guard: block any unexpected form submissions which cause full page reloads.
        document.addEventListener('submit', function(e) {
            try {
                const id = e.target && e.target.id ? e.target.id : '(no-id)';
                if (id !== 'formModificarDatos') {
                    e.preventDefault();
                    e.stopPropagation();
                    console.warn(`Blocked unexpected form submit on #${id}`);
                }
            } catch (ex) {
                // swallow
            }
        }, true);

        const evento = sessionStorage.getItem('eventoSeleccionado');
        const series = sessionStorage.getItem('seriesTemporales');
        const alcanceSismos = sessionStorage.getItem('ultimosAlcances');
        const origenesGeneracion = sessionStorage.getItem('ultimosOrigenes');
    // cargar datos desde sessionStorage
        try {
            pantalla.mostrarDatosSismicos(JSON.parse(evento), JSON.parse(series), JSON.parse(alcanceSismos), JSON.parse(origenesGeneracion));
        } catch (e) {
            console.error('scriptDatosEvento: error parseando datos de sessionStorage', e);
            pantalla.mostrarDatosSismicos(null, [], [], []);
        }
        // Debug helper: capture navigation-causing clicks to see what triggers reloads.
        // Set to `true` while debugging to block and log navigations; flip to false to restore normal behavior.
    // Disable verbose debug navigation helpers in production usage
    const debugBlockNavigation = false;
        // Console persistence: wrap console methods to keep messages across reloads in sessionStorage.
        if (debugBlockNavigation) {
            (function() {
                try {
                    const maxMessages = 200;
                    const orig = { log: console.log.bind(console), warn: console.warn.bind(console), error: console.error.bind(console), debug: console.debug ? console.debug.bind(console) : console.log.bind(console) };
                    const pushMessage = (level, args) => {
                        try {
                            const raw = sessionStorage.getItem('debugConsoleMessages');
                            const arr = raw ? JSON.parse(raw) : [];
                            arr.push({ level, args: Array.from(args) });
                            if (arr.length > maxMessages) arr.splice(0, arr.length - maxMessages);
                            sessionStorage.setItem('debugConsoleMessages', JSON.stringify(arr));
                        } catch (e) {
                            // ignore
                        }
                    };
                    console.log = function() { pushMessage('log', arguments); orig.log.apply(console, arguments); };
                    console.warn = function() { pushMessage('warn', arguments); orig.warn.apply(console, arguments); };
                    console.error = function() { pushMessage('error', arguments); orig.error.apply(console, arguments); };
                    console.debug = function() { pushMessage('debug', arguments); orig.debug.apply(console, arguments); };
                } catch (e) {
                    console.error('Could not wrap console for persistence', e);
                }
            })();
        }
        // We will NOT attempt to override read-only window.location methods (assign/replace/reload)
        // because many browsers make these properties non-writable and overriding throws.
        // no-op debug message when disabled
        if (debugBlockNavigation) {
            document.addEventListener('click', function(ev) {
                try {
                    const t = ev.target;
                    // Find nearest anchor or button
                    const anchor = t.closest ? t.closest('a') : null;
                    const button = t.closest ? t.closest('button') : null;
                    if (anchor && anchor.getAttribute && anchor.getAttribute('href')) {
                        console.warn('DebugNav: anchor clicked (not blocked)', { href: anchor.getAttribute('href'), text: anchor.textContent, stack: new Error().stack });
                    }
                    if (button && button.type === 'submit') {
                        console.warn('DebugNav: submit-button clicked (not blocked)', { id: button.id, type: button.type, stack: new Error().stack });
                    }
                } catch (err) {
                    // ignore
                }
            }, true);
            // Also log unload-related events with stack traces; persist them so logs survive reload
            window.addEventListener('beforeunload', function(e) {
                try {
                    console.warn('DebugNav: beforeunload fired', new Error().stack);
                    const raw = sessionStorage.getItem('debugConsoleMessages') || '[]';
                    const arr = JSON.parse(raw);
                    arr.push({ level: 'warn', args: ['DebugNav: beforeunload persisted', new Error().stack] });
                    sessionStorage.setItem('debugConsoleMessages', JSON.stringify(arr));
                } catch (err) {
                    try { console.error('DebugNav: beforeunload handler error', err); } catch(_){}
                }
            });

            window.addEventListener('pagehide', function(e) {
                try {
                    console.warn('DebugNav: pagehide fired', { persisted: e.persisted, stack: new Error().stack });
                    const raw = sessionStorage.getItem('debugConsoleMessages') || '[]';
                    const arr = JSON.parse(raw);
                    arr.push({ level: 'warn', args: ['DebugNav: pagehide persisted', e.persisted, new Error().stack] });
                    sessionStorage.setItem('debugConsoleMessages', JSON.stringify(arr));
                } catch (err) {
                    try { console.error('DebugNav: pagehide handler error', err); } catch(_){}
                }
            });
        }
        pantalla.mostrarOpcionMapa();
        const btnMapa = document.getElementById('btnMapa');
        btnMapa.addEventListener('click', function() {
            pantalla.tomarSeleccionDeOpcionMapa();
        });
        pantalla.pedirOpcionModificarDatos();
        pantalla.pedirOpcionEvento();

        // Enlazar botones de acción rápida (Confirmar, Derivar, Rechazar) mostrando
        // un modal de confirmación antes de ejecutar la acción.
    const btnConfirmar = document.getElementById('btnConfirmar');
    const btnDerivar = document.getElementById('btnDerivar');
    const btnRechazar = document.getElementById('btnRechazar');

            const showConfirmModal = (actionKey, actionLabel) => {
            const modalEl = document.getElementById('confirmActionModal');
            if (!modalEl) {
                pantalla.ejecutarAccion(actionKey);
                return;
            }
            const modalTitle = modalEl.querySelector('.modal-title');
            const modalText = modalEl.querySelector('#confirmModalText');
            const confirmBtn = modalEl.querySelector('#confirmActionBtn');
            // show confirm modal
            modalTitle.textContent = actionLabel;
            // Construir un texto más natural: quitar palabra 'evento' si está al final del label
            const labelShort = actionLabel.replace(/\s*evento\s*$/i, '').toLowerCase();
            modalText.textContent = `¿Desea ${labelShort} este evento?`;

            const bsModal = new bootstrap.Modal(modalEl, { keyboard: true });
            // Ajustar estilos del botón Confirmar según la acción
            const actionBtnClasses = {
                'confirmar': 'btn btn-success btn-lg',
                'experto': 'btn btn-warning btn-lg',
                'rechazar': 'btn btn-danger btn-lg'
            };
            try {
                // cancelar: buscar el botón que cierra el modal
                const cancelBtn = modalEl.querySelector('.btn-outline-secondary') || modalEl.querySelector('[data-bs-dismiss="modal"]');
                if (cancelBtn) cancelBtn.className = 'btn btn-secondary btn-lg';
            } catch (e) {
                // ignore
            }

            // Remover handlers previos: clonar el botón para eliminar listeners y asignar nuevo handler
            const newConfirm = confirmBtn.cloneNode(true);
            confirmBtn.parentNode.replaceChild(newConfirm, confirmBtn);
            newConfirm.className = actionBtnClasses[actionKey] || 'btn btn-primary btn-lg';
                newConfirm.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                bsModal.hide();
                pantalla.ejecutarAccion(actionKey);
            });
            bsModal.show();
            // Focus accessibility: focus the confirm button
            setTimeout(() => { newConfirm.focus(); }, 200);
        };

    if (btnConfirmar) btnConfirmar.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); showConfirmModal('confirmar', 'Confirmar evento'); });
    if (btnDerivar) btnDerivar.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); showConfirmModal('experto', 'Derivar a experto'); });
    if (btnRechazar) btnRechazar.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); showConfirmModal('rechazar', 'Rechazar evento'); });
    });


    // El control por botón único fue reemplazado por acciones rápidas.

    const formModificar = document.getElementById('formModificarDatos');
    if (formModificar) {
        formModificar.addEventListener('submit', function(e) {
            e.preventDefault();
            pantalla.tomarOpcionModificacionDatos();
        });
    }

    const btnVolver = document.getElementById('btnVolver');
    if (btnVolver) {
        btnVolver.addEventListener('click', async () => {
            try {
                // 1. Mostrar loading y deshabilitar
                pantalla.showLoading('Liberando evento...');

                // 2. Llamar al backend para revertir el estado
                const response = await fetch(`${API_BASE}/cancelar_revision`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                
                const data = await response.json();
                
                // 3. Manejo de respuesta
                if (data.success) {
                    // Éxito: limpiar sesión y redirigir
                    sessionStorage.removeItem('eventoSeleccionado');
                    // Mostrar mensaje de éxito no bloqueante (opcional)
                    window.location.href = 'registrar.html';
                } else {
                    // Fallo (ej: no había evento seleccionado o error de persistencia)
                    alert(data.error || 'Error desconocido al cancelar.');
                    // Redirigir de todas formas para limpiar la vista actual
                    window.location.href = 'registrar.html';
                }
            } catch (error) {
                console.error('Error al cancelar revisión:', error);
                alert('Error de conexión con el servidor al cancelar revisión.');
                // Fallback
                window.location.href = 'registrar.html';
            } finally {
                pantalla.hideLoading();
            }
        });
    }

