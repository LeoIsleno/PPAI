const API_BASE = 'http://127.0.0.1:5001';
import { PantallaRevisionManual } from "./PantallaRevisionManual.js";
const pantalla = new PantallaRevisionManual();

    document.addEventListener('DOMContentLoaded', function() { 
        const evento = sessionStorage.getItem('eventoSeleccionado');
        const series = sessionStorage.getItem('seriesTemporales');
        const alcanceSismos = sessionStorage.getItem('ultimosAlcances');
        const origenesGeneracion = sessionStorage.getItem('ultimosOrigenes');
        pantalla.mostrarDatosSismicos(JSON.parse(evento), JSON.parse(series), JSON.parse(alcanceSismos), JSON.parse(origenesGeneracion));
        pantalla.pedirOpcionEveneto();
    });

    // Botones de opciones
    const btnMapa = document.getElementById('btnMapa');
    if (btnMapa) {
        btnMapa.addEventListener('click', function() {
            // tu código
        });
    }

    const btnEjecutarAccion = document.getElementById('btnEjecutarAccion');
    if (btnEjecutarAccion) {
        btnEjecutarAccion.addEventListener('click', function() {
            pantalla.tomarSeleccionOpcionEvento();
        });
    }

//TODO: ESTO CREO QUE NO DEBE QUEDAR ASÍ
(function() {
    const formModificar = document.getElementById('formModificarDatos');
    if (formModificar) {
        formModificar.addEventListener('submit', function(e) {
            e.preventDefault();
            const valorMagnitud = document.getElementById('inputMagnitud').value;
            const alcanceSismo = document.getElementById('inputAlcance').value;
            const origenGeneracion = document.getElementById('inputOrigen').value;
            fetch(`${API_BASE}/modificar_datos_evento`, {
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

