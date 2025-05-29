document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const usuario = document.getElementById('usuario').value;
        const contrasena = document.getElementById('contrasena').value;

        if (usuario === '123' && contrasena === '456') {
            fetch('/opciones')
                .then(response => {
                    if (response.ok) {
                        window.location.href = '/opciones';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    errorMessage.textContent = 'Error al intentar redirigir';
                    errorMessage.style.display = 'block';
                });
        } else {
            errorMessage.textContent = 'Usuario o contraseña incorrectos.';
            errorMessage.style.display = 'block';
        }
    });
});