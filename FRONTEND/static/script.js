import { PantallaRevisionManual } from "./PantallaRevisionManual.js";
const pantalla = new PantallaRevisionManual();
const btnRegistrar = document.getElementById('btnRegistrar');

window.addEventListener('DOMContentLoaded', async () => {
   pantalla.mostrarEventosSismicos();
   pantalla.solicitarEventoSismico();
});

btnRegistrar.addEventListener('click', function () {
   pantalla.tomarSeleccionDeEventoSismico();
});





