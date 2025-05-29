document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logoutButton');
    
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            if (confirm('¿Está seguro que desea cerrar sesión?')) {
                window.location.href = '/';
            }
        });
    }
});