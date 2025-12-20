// ========================================
// Login Page JavaScript
// ========================================

const API_BASE_URL = 'http://localhost:5000';

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const messageDiv = document.getElementById('message');
    
    // Clear previous messages
    messageDiv.textContent = '';
    messageDiv.className = 'message';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (data.success) {
            messageDiv.textContent = `Welcome ${data.user.name}!`;
            messageDiv.className = 'message success';
            
            // Redirect based on role after 1 second
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        } else {
            messageDiv.textContent = data.error || 'Login failed';
            messageDiv.className = 'message error';
        }
    } catch (error) {
        messageDiv.textContent = 'Connection error. Please ensure the server is running.';
        messageDiv.className = 'message error';
        console.error('Login error:', error);
    }
});
