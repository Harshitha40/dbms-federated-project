// ========================================
// Admin Panel JavaScript
// ========================================

const API_BASE_URL = '';

window.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await loadUsers();
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
        if (!data.success || data.user.role !== 'Administrator') {
            alert('Access denied. Administrator role required.');
            window.location.href = 'dashboard.html';
        }
    } catch (error) {
        console.error('Auth check error:', error);
        window.location.href = 'login.html';
    }
}

function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));

    document.getElementById(`${tabName}Tab`).classList.add('active');
    event.target.classList.add('active');

    if (tabName === 'logs') {
        loadQueryLogs();
    }
}

// Create User Form
document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const messageDiv = document.getElementById('createUserMessage');
    messageDiv.textContent = '';
    messageDiv.className = 'message';

    const data = {
        name: document.getElementById('user_name').value,
        email: document.getElementById('user_email').value,
        password: document.getElementById('user_password').value,
        role: document.getElementById('user_role').value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            messageDiv.textContent = 'User created successfully!';
            messageDiv.className = 'message success';
            document.getElementById('createUserForm').reset();
            await loadUsers();
        } else {
            messageDiv.textContent = result.error || 'Failed to create user';
            messageDiv.className = 'message error';
        }
    } catch (error) {
        messageDiv.textContent = 'Connection error';
        messageDiv.className = 'message error';
        console.error('Create user error:', error);
    }
});

async function loadUsers() {
    const container = document.getElementById('usersList');
    container.innerHTML = '<p>Loading users...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/users`, {
            credentials: 'include'
        });

        const data = await response.json();

        if (data.success) {
            displayUsers(data.users);
        } else {
            container.innerHTML = '<p class="error">Failed to load users</p>';
        }
    } catch (error) {
        container.innerHTML = '<p class="error">Connection error</p>';
        console.error('Load users error:', error);
    }
}

function displayUsers(users) {
    const container = document.getElementById('usersList');

    if (!users || users.length === 0) {
        container.innerHTML = '<p>No users found</p>';
        return;
    }

    let tableHTML = '<table class="results-table">';
    tableHTML += '<thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th><th>Created</th><th>Actions</th></tr></thead>';
    tableHTML += '<tbody>';

    users.forEach(user => {
        const createdDate = new Date(user.created_at).toLocaleDateString();
        tableHTML += `
            <tr>
                <td>${user.user_id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
                <td><span class="badge">${user.role}</span></td>
                <td>${createdDate}</td>
                <td>
                    <button onclick="deleteUser(${user.user_id}, '${user.name}')" class="btn btn-danger btn-small">Delete</button>
                </td>
            </tr>
        `;
    });

    tableHTML += '</tbody></table>';
    container.innerHTML = tableHTML;
}

async function deleteUser(userId, userName) {
    if (!confirm(`Are you sure you want to delete user "${userName}"?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/users/${userId}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        const result = await response.json();

        if (result.success) {
            alert('User deleted successfully');
            await loadUsers();
        } else {
            alert('Failed to delete user: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Connection error');
        console.error('Delete user error:', error);
    }
}

async function loadQueryLogs() {
    const container = document.getElementById('queryLogsList');
    container.innerHTML = '<p>Loading query logs...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/query-logs?limit=50`, {
            credentials: 'include'
        });

        const data = await response.json();

        if (data.success) {
            displayQueryLogs(data.logs);
        } else {
            container.innerHTML = '<p class="error">Failed to load query logs</p>';
        }
    } catch (error) {
        container.innerHTML = '<p class="error">Connection error</p>';
        console.error('Load logs error:', error);
    }
}

function displayQueryLogs(logs) {
    const container = document.getElementById('queryLogsList');

    if (!logs || logs.length === 0) {
        container.innerHTML = '<p>No query logs found</p>';
        return;
    }

    let tableHTML = '<table class="results-table">';
    tableHTML += '<thead><tr><th>ID</th><th>User</th><th>Role</th><th>Query</th><th>Executed At</th></tr></thead>';
    tableHTML += '<tbody>';

    logs.forEach(log => {
        const executedDate = new Date(log.executed_at).toLocaleString();
        const queryPreview = log.query_text.length > 100
            ? log.query_text.substring(0, 100) + '...'
            : log.query_text;

        tableHTML += `
            <tr>
                <td>${log.query_id}</td>
                <td>${log.user_name}<br><small>${log.user_email}</small></td>
                <td><span class="badge">${log.user_role}</span></td>
                <td><code class="query-preview">${queryPreview}</code></td>
                <td>${executedDate}</td>
            </tr>
        `;
    });

    tableHTML += '</tbody></table>';
    container.innerHTML = tableHTML;
}

async function logout() {
    try {
        await fetch(`${API_BASE_URL}/api/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        window.location.href = 'login.html';
    } catch (error) {
        window.location.href = 'login.html';
    }
}
