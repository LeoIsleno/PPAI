// Verificar autenticación en todas las páginas excepto login
function checkAuth() {
    const currentPage = window.location.pathname.split('/').pop();
    
    if (currentPage === 'login.html' || currentPage === '') return;
    
    const session = localStorage.getItem('seismicSession') || sessionStorage.getItem('seismicSession');
    
    if (!session) {
        window.location.href = 'login.html';
        return;
    }
    
    const data = JSON.parse(session);
    const loginTime = new Date(data.loginTime);
    const now = new Date();
    const hoursDiff = (now - loginTime) / (1000 * 60 * 60);
    
    // Sesión expira en 24 horas
    if (hoursDiff >= 24) {
        localStorage.removeItem('seismicSession');
        sessionStorage.removeItem('seismicSession');
        window.location.href = 'login.html';
        return;
    }
    
    // Actualizar información del usuario en la UI
    const userNameElement = document.getElementById('userName');
    if (userNameElement) {
        userNameElement.textContent = data.username;
    }
}

// Función para cerrar sesión
function logout() {
    if (confirm('¿Está seguro que desea cerrar sesión?')) {
        localStorage.removeItem('seismicSession');
        sessionStorage.removeItem('seismicSession');
        window.location.href = 'login.html';
    }
}

// Verificar autenticación al cargar la página
window.addEventListener('DOMContentLoaded', checkAuth);
