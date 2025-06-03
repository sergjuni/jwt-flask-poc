// app/static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const messageArea = document.getElementById('messageArea');
    const protectedDataArea = document.getElementById('protectedDataArea');
    const fetchProtectedDataButton = document.getElementById('fetchProtectedDataButton');
    const logoutButton = document.getElementById('logoutButton');

    const API_BASE_URL = '/auth';

    function showMessage(message, isError = false) {
        messageArea.textContent = message;
        messageArea.className = isError ? 'error' : 'success';
    }

    function updateUIForLoggedInState(isLoggedIn) {
        if (isLoggedIn) {
            fetchProtectedDataButton.style.display = 'block';
            logoutButton.style.display = 'block';
            loginForm.style.display = 'none';
            registerForm.style.display = 'none';
        } else {
            fetchProtectedDataButton.style.display = 'none';
            logoutButton.style.display = 'none';
            protectedDataArea.textContent = '';
            loginForm.style.display = 'block';
            registerForm.style.display = 'block';
        }
    }

    if (localStorage.getItem('jwtToken')) {
        updateUIForLoggedInState(true);
    } else {
        updateUIForLoggedInState(false);
    }

    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('regUsername').value;
        const password = document.getElementById('regPassword').value;
        try {
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (response.ok) {
                showMessage(`Usuário registrado: ${data.msg} (ID: ${data.id})`);
                registerForm.reset();
            } else {
                showMessage(`Erro no registro: ${data.msg}`, true);
            }
        } catch (error) {
            showMessage(`Erro de conexão: ${error.message}`, true);
        }
    });

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await response.json();
            if (response.ok) {
                localStorage.setItem('jwtToken', data.access_token);
                showMessage('Login realizado com sucesso!');
                updateUIForLoggedInState(true);
                loginForm.reset();
            } else {
                showMessage(`Erro no login: ${data.msg}`, true);
                updateUIForLoggedInState(false);
            }
        } catch (error) {
            showMessage(`Erro de conexão: ${error.message}`, true);
            updateUIForLoggedInState(false);
        }
    });

    fetchProtectedDataButton.addEventListener('click', async () => {
        const token = localStorage.getItem('jwtToken');
        if (!token) {
            showMessage('Token não encontrado. Faça login novamente.', true);
            updateUIForLoggedInState(false);
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/protected`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            if (response.ok) {
                protectedDataArea.textContent = `Dados protegidos: Logado como ${data.logged_in_as} (ID: ${data.user_id})`;
                showMessage('Dados protegidos carregados.');
            } else {
                showMessage(`Erro ao buscar dados: ${data.msg}`, true);
                if (response.status === 401 || response.status === 422) {
                    localStorage.removeItem('jwtToken');
                    updateUIForLoggedInState(false);
                }
            }
        } catch (error) {
            showMessage(`Erro de conexão: ${error.message}`, true);
        }
    });

    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('jwtToken');
        showMessage('Logout realizado.');
        updateUIForLoggedInState(false);
    });
});