import { PantallaRevisionManual } from "./PantallaRevisionManual.js";
const pantalla = new PantallaRevisionManual();
const btnRegistrar = document.getElementById('btnRegistrar');

window.addEventListener('DOMContentLoaded', async () => {
   pantalla.mostrarEventosSismicos();
});

btnRegistrar.addEventListener('click', function () {
   pantalla.solicitarEventoSismico();
   pantalla.tomarSeleccionEventoSismico();
})





