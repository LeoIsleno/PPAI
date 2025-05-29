class PantallaRevisionManual {

    constructor(cboEventoSismicos) {
        self.cboEventoSismicos = cboEventoSismicos;
    }

    async OpRegistrarResultadoRevisionManual() {
        const newWindow = window.open('registrar.html', '_self');
    };


    async mostrarEventosSismicos() {
        const select = document.getElementById('evento');
        const mensaje = document.getElementById('mensajeEventos');

        try {
            const response = await fetch('http://localhost:5001/');
            const eventos = await response.json();

            // Limpia las opciones previas excepto la primera
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
        } catch (error) {
            mensaje.textContent = 'Error al cargar los eventos sísmicos.';
            mensaje.classList.remove('d-none');
        }
    }

    solicitarEventoSismico() {
        const evento = document.getElementById("evento");
        self.cboEventoSismicos = evento;
    }

    tomarSeleccionEventoSismico() {
        const valor = self.cboEventoSismicos.value;
        const evento = JSON.parse(valor);

        // Usá 127.0.0.1 y pasá el nombre correcto del parámetro
        fetch('http://localhost:5001/seleccionar_evento', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ evento })
        })
            .then(r => r.json())
            .then(data => {
                if (data.success && data.redirect) {
                    window.location.href = data.redirect;
                    console.log("Redirigiendo a:", data.redirect);
                } else {
                    alert(data.error || 'Error al seleccionar el evento');
                }
            });
    }


}

export { PantallaRevisionManual };





