import {PantallaRevisionManual} from './PantallaRevisionManual.js';

const pantalla = new PantallaRevisionManual();

document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logoutButton');
    const btnOpcionRevision = document.getElementById('registrarRevisionBtn');

    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            if (confirm('¿Está seguro que desea cerrar sesión?')) {
                window.location.href = '/';
            }
        });
    }

    if (btnOpcionRevision) {
        btnOpcionRevision.addEventListener('click', function() {
            console.log('Opción de registrar revisión manual seleccionada');
            pantalla.OpRegistrarResultadoRevisionManual();
        });
    }
});

