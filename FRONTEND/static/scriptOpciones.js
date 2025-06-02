import {PantallaRevisionManual} from './PantallaRevisionManual.js';

const pantalla = new PantallaRevisionManual();

document.addEventListener('DOMContentLoaded', function() {
    const btnOpcionRevision = document.getElementById('registrarRevisionBtn');


    if (btnOpcionRevision) {
        btnOpcionRevision.addEventListener('click', function() {
            console.log('Opción de registrar revisión manual seleccionada');
            pantalla.opRegistrarResultadoRevisionManual();
        });
    }
});

