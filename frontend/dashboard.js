// ========================================
// Dashboard JavaScript
// ========================================

const API_BASE_URL = 'http://localhost:5000';
let currentUser = null;

// Check authentication on page load
window.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await checkDatabaseStatus();
    showRoleBasedContent();
});

async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/current-user`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            window.location.href = 'login.html';
            return;
        }
        
        const data = await response.json();
        if (data.success) {
            currentUser = data.user;
            document.getElementById('userName').textContent = currentUser.name;
            document.getElementById('userRole').textContent = currentUser.role;
            document.getElementById('userInfo').textContent = `${currentUser.name} (${currentUser.role})`;
        } else {
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error('Auth check error:', error);
        window.location.href = 'login.html';
    }
}

function showRoleBasedContent() {
    const queryCard = document.getElementById('queryCard');
    const providerCard = document.getElementById('providerCard');
    const adminCard = document.getElementById('adminCard');
    
    // Show/hide cards based on role
    if (currentUser.role === 'Researcher') {
        queryCard.style.display = 'block';
        providerCard.style.display = 'none';
        adminCard.style.display = 'none';
    } else if (currentUser.role === 'Data Provider') {
        queryCard.style.display = 'none';
        providerCard.style.display = 'block';
        adminCard.style.display = 'none';
    } else if (currentUser.role === 'Administrator') {
        queryCard.style.display = 'block';
        providerCard.style.display = 'block';
        adminCard.style.display = 'block';
    }
}

async function checkDatabaseStatus() {
    const statusDiv = document.getElementById('dbStatus');
    statusDiv.innerHTML = '<p>Checking database connections...</p>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/database-status`, {
            credentials: 'include'
        });
        
        const data = await response.json();
        
        if (data.success) {
            const status = data.status;
            statusDiv.innerHTML = `
                <div class="status-item">
                    <span class="status-label">PostgreSQL:</span>
                    <span class="status-badge ${status.postgres ? 'status-online' : 'status-offline'}">
                        ${status.postgres ? '✓ Connected' : '✗ Offline'}
                    </span>
                </div>
                <div class="status-item">
                    <span class="status-label">MongoDB:</span>
                    <span class="status-badge ${status.mongodb ? 'status-online' : 'status-offline'}">
                        ${status.mongodb ? '✓ Connected' : '✗ Offline'}
                    </span>
                </div>
                <div class="status-item">
                    <span class="status-label">Apache Drill:</span>
                    <span class="status-badge ${status.drill ? 'status-online' : 'status-offline'}">
                        ${status.drill ? '✓ Connected' : '✗ Offline'}
                    </span>
                </div>
            `;
        } else {
            statusDiv.innerHTML = '<p class="error">Failed to check database status</p>';
        }
    } catch (error) {
        statusDiv.innerHTML = '<p class="error">Error connecting to server</p>';
        console.error('Status check error:', error);
    }
}

async function logout() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        
        if (response.ok) {
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error('Logout error:', error);
        // Redirect anyway
        window.location.href = 'login.html';
    }
}
