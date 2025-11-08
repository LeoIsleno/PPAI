document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');
    
    errorAlert.classList.add('d-none');
    
    // Validación simple del lado del cliente
    if (!username || !password) {
        errorMessage.textContent = 'Por favor complete todos los campos';
        errorAlert.classList.remove('d-none');
        return;
    }
    
    // Credenciales de prueba - En producción esto debe ir al backend
    const validUsers = {
        'nico': '123',
        'admin': 'admin123',
        'analista': 'analista123'
    };
    
    if (validUsers[username] && validUsers[username] === password) {
        // Guardar sesión
        const sessionData = {
            username: username,
            loginTime: new Date().toISOString(),
            rememberMe: rememberMe
        };
        
        if (rememberMe) {
            localStorage.setItem('seismicSession', JSON.stringify(sessionData));
        } else {
            sessionStorage.setItem('seismicSession', JSON.stringify(sessionData));
        }
        
        // Animación de éxito
        const button = e.target.querySelector('button[type="submit"]');
        button.innerHTML = '<i class="bi bi-check-circle-fill me-2"></i>Acceso exitoso';
        button.classList.add('btn-success');
        
        // Redirigir al panel principal
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 800);
    } else {
        errorMessage.textContent = 'Usuario o contraseña incorrectos';
        errorAlert.classList.remove('d-none');
        
        // Animación de shake en el formulario
        const card = document.querySelector('.login-card');
        card.style.animation = 'shake 0.5s';
        setTimeout(() => {
            card.style.animation = '';
        }, 500);
    }
});

// Animación de shake
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
`;
document.head.appendChild(style);

// Verificar si ya hay sesión activa
window.addEventListener('DOMContentLoaded', () => {
    const session = localStorage.getItem('seismicSession') || sessionStorage.getItem('seismicSession');
    if (session) {
        const data = JSON.parse(session);
        const loginTime = new Date(data.loginTime);
        const now = new Date();
        const hoursDiff = (now - loginTime) / (1000 * 60 * 60);
        
        // Si la sesión tiene menos de 24 horas, redirigir
        if (hoursDiff < 24) {
            window.location.href = 'index.html';
        } else {
            // Limpiar sesión expirada
            localStorage.removeItem('seismicSession');
            sessionStorage.removeItem('seismicSession');
        }
    }
});
