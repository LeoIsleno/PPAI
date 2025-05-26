document.addEventListener('DOMContentLoaded', function () {
    // Obtener referencias a los elementos del DOM
    const form = document.getElementById('selectEventForm');
    const select = document.getElementById('evento');
    const mensajeEventos = document.getElementById('mensajeEventos');
    const cancelButton = document.getElementById('cancelButton');

    // Verificar si hay eventos disponibles
    if (select.options.length <= 1) {
        mostrarMensaje('No hay eventos disponibles para revisión');
        select.disabled = true;
    }

    // Manejar el envío del formulario
    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault();

            try {
                // Obtener datos del evento seleccionado
                const eventoData = JSON.parse(select.value);

                // Enviar selección al servidor
                const response = await fetch('/seleccionar_evento', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({evento_id: eventoData.id})
                });

                const data = await response.json();

                // Redireccionar si fue exitoso
                if (data.success && data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    throw new Error(data.error || 'Error desconocido');
                }
            } catch (error) {
                mostrarMensaje('Error: ' + error.message);
            }
        });
    }

    // Manejar el botón cancelar
    if (cancelButton) {
        cancelButton.addEventListener('click', function (event) {
            event.preventDefault();
            if (confirm('¿Desea cancelar la operación?')) {
                window.location.href = '/opciones';
            }
        });
    }

    // Función auxiliar para mostrar mensajes
    function mostrarMensaje(mensaje) {
        mensajeEventos.textContent = mensaje;
        mensajeEventos.classList.remove('d-none');
    }

    // Agregar evento change al select
    select.addEventListener('change', function () {
        try {
            //const eventoData = JSON.parse(this.value);
            // Enviar el formulario automáticamente
            //mostrarDetallesEvento(eventoData);

            form.requestSubmit();  // Esto dispara el evento 'submit'

        } catch (error) {
            console.error('Error al parsear datos:', error);
            ocultarDetallesEvento();
        }
    });

    /*
        // Función para mostrar detalles del evento
        function mostrarDetallesEvento(evento) {
            const detalles = document.getElementById('detallesEvento');

            // Actualizar datos
            document.getElementById('fechaHora').textContent = evento.fechaHoraOcurrencia;
            document.getElementById('magnitud').textContent = evento.valorMagnitud;
            document.getElementById('epicentro').textContent =
                `(${evento.latitudEpicentro}, ${evento.longitudEpicentro})`;
            document.getElementById('hipocentro').textContent =
                `(${evento.latitudHipocentro}, ${evento.longitudHipocentro})`;

            // Mostrar el div de detalles
            detalles.classList.remove('d-none');
        }*/

    // Función para ocultar detalles
    function ocultarDetallesEvento() {
        const detalles = document.getElementById('detallesEvento');
        detalles.classList.add('d-none');
    }
});