document.addEventListener('DOMContentLoaded', function() {
    console.log('Cargando datos del evento...'); // Debug

    // Obtener datos del evento
    fetch('/obtener_datos_evento')
        .then(response => {
            console.log('Respuesta recibida:', response); // Debug
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data); // Debug
            if (data.success) {
                mostrarDatosEvento(data.evento);
            } else {
                throw new Error(data.error || 'Error desconocido');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarError('Error al cargar los datos del evento: ' + error.message);
        });

    // Botones de opciones
    document.getElementById('btnMapa').addEventListener('click', function() {
        if (!confirm('¿Desea ver el mapa del evento?')) {
            return;
        }
        fetch('/mostrar_mapa');
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
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ accion: accion })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Acción ejecutada con éxito');
                window.location.href = '/opciones';
            }
        });
    });
});

function mostrarDatosEvento(evento) {
    console.log('Mostrando datos:', evento); // Debug
    
    const datosPrincipales = document.getElementById('datosPrincipales');
    if (!evento) {
        mostrarError('No se pudieron cargar los datos del evento');
        return;
    }

    // Duplicado de la información del evento
    datosPrincipales.innerHTML += `
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
}

function mostrarError(mensaje) {
    const datosPrincipales = document.getElementById('datosPrincipales');
    datosPrincipales.innerHTML = `
        <div class="alert alert-danger">
            ${mensaje}
        </div>
    `;
}