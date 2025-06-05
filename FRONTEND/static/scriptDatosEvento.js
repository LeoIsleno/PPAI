const API_BASE = 'http://127.0.0.1:5001';
import { PantallaRevisionManual } from "./PantallaRevisionManual.js";
const pantalla = new PantallaRevisionManual();

    document.addEventListener('DOMContentLoaded', function() { 
        const evento = sessionStorage.getItem('eventoSeleccionado');
        const series = sessionStorage.getItem('seriesTemporales');
        const alcanceSismos = sessionStorage.getItem('ultimosAlcances');
        const origenesGeneracion = sessionStorage.getItem('ultimosOrigenes');
        pantalla.mostrarDatosSismicos(JSON.parse(evento), JSON.parse(series), JSON.parse(alcanceSismos), JSON.parse(origenesGeneracion));
        pantalla.mostrarOpcionMapa();
        const btnMapa = document.getElementById('btnMapa');
        btnMapa.addEventListener('click', function() {
            pantalla.tomarSeleccionDeOpcionMapa();
        });
        pantalla.pedirOpcionModificarDatos();
        pantalla.pedirOpcionEvento();
    });


    const btnEjecutarAccion = document.getElementById('btnEjecutarAccion');
    if (btnEjecutarAccion) {
        btnEjecutarAccion.addEventListener('click', function() {
            pantalla.tomarSeleccionOpcionEvento();
        });
    }

    const formModificar = document.getElementById('formModificarDatos');
    if (formModificar) {
        formModificar.addEventListener('submit', function(e) {
            e.preventDefault();
            pantalla.tomarOpcionModificacionDatos();
        });
    }


