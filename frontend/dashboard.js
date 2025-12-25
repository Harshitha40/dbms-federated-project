// ========================================
// Dashboard JavaScript
// ========================================

const API_BASE_URL = '';
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
    const defaultDashboard = document.getElementById('defaultDashboard');
    const providerDashboard = document.getElementById('providerDashboard');
    const infoSection = document.querySelector('.info-section');
    const queryCard = document.getElementById('queryCard');
    const providerCard = document.getElementById('providerCard');
    const adminCard = document.getElementById('adminCard');
    const navAdmin = document.getElementById('navAdmin');

    // Hide admin nav link for everyone except Administrator
    if (navAdmin) {
        navAdmin.style.display = currentUser.role === 'Administrator' ? 'block' : 'none';
    }

    if (currentUser.role === 'Data Provider') {
        defaultDashboard.style.display = 'none';
        infoSection.style.display = 'none';
        providerDashboard.style.display = 'block';
    } else {
        defaultDashboard.style.display = 'grid';
        infoSection.style.display = 'block';
        providerDashboard.style.display = 'none';

        // Refined card visibility for other roles
        if (currentUser.role === 'Researcher') {
            queryCard.style.display = 'block';
            providerCard.style.display = 'none';
            adminCard.style.display = 'none';
        } else if (currentUser.role === 'Administrator') {
            queryCard.style.display = 'block';
            providerCard.style.display = 'block';
            adminCard.style.display = 'block';
        }
    }
}

async function executeProviderQuery() {
    const naturalInput = document.getElementById('providerQueryInput').value.trim();
    const messageDiv = document.getElementById('providerMessage');
    const resultsArea = document.getElementById('providerResultsArea');

    if (!naturalInput) {
        messageDiv.textContent = 'Please enter a question about your data.';
        messageDiv.className = 'message error';
        messageDiv.style.display = 'block';
        return;
    }

    messageDiv.textContent = '🤖 Processing your question...';
    messageDiv.className = 'message info';
    messageDiv.style.display = 'block';
    resultsArea.innerHTML = '';

    try {
        const response = await fetch(`${API_BASE_URL}/api/natural-query`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ query: naturalInput })
        });

        const data = await response.json();

        if (data.success) {
            messageDiv.textContent = `✓ AI Success: ${(data.confidence * 100).toFixed(0)}% confidence`;
            messageDiv.className = 'message success';
            displayProviderResults(data.data);
        } else {
            messageDiv.textContent = data.error || 'The AI could not answer this. Try rephrasing.';
            messageDiv.className = 'message error';
        }
    } catch (error) {
        messageDiv.textContent = 'Connection error. Ensure the platform backend is running.';
        messageDiv.className = 'message error';
        console.error('NLP error:', error);
    }
}

function displayProviderResults(data) {
    const resultsArea = document.getElementById('providerResultsArea');
    if (!data || data.length === 0) {
        resultsArea.innerHTML = '<p class="message info" style="display:block">The query returned no records.</p>';
        return;
    }

    const columns = Object.keys(data[0]);
    let html = '<div style="overflow-x: auto;"><table class="data-table" style="width:100%"><thead><tr>';
    columns.forEach(col => {
        html += `<th style="text-align:left; padding:12px; border-bottom:2px solid #111; text-transform:uppercase; font-size:0.75rem;">${col}</th>`;
    });
    html += '</tr></thead><tbody>';

    data.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            let val = row[col];
            if (val === null || val === undefined) val = '-';
            else if (typeof val === 'object') val = JSON.stringify(val);
            html += `<td style="padding:12px; border-bottom:1px solid #EEE; font-size:0.85rem;">${val}</td>`;
        });
        html += '</tr>';
    });

    html += '</tbody></table></div>';
    resultsArea.innerHTML = html;
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
