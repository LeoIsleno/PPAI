class PantallaRevisionManual {

    async OpRegistrarResultadoRevisionManual() {
        const newWindow = window.open('registrar.html', '_self');


            const data = await fetch('http://localhost:5001/');
            const dataJson = await data.json();

            // Send the data to the new window using postMessage
            console.log(dataJson);
        };  
        

        async mostrarDatos() {
        const data = await fetch('http://localhost:5001/');
        const dataJson = await data.json();
        console.log('Mostrando datos de eventos:',dataJson);
        }

    }

export { PantallaRevisionManual };

