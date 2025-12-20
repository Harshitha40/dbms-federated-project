// ========================================
// Data Provider Interface JavaScript
// ========================================

const API_BASE_URL = 'http://localhost:5000';

window.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await loadRegions();
});

async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/current-user`, {
            credentials: 'include'
        });
        
        if (!response.ok) {
            window.location.href = 'login.html';
        }
    } catch (error) {
        console.error('Auth check error:', error);
        window.location.href = 'login.html';
    }
}

async function loadRegions() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/regions`, {
            credentials: 'include'
        });
        
        const data = await response.json();
        
        if (data.success) {
            populateRegionDropdowns(data.regions);
        }
    } catch (error) {
        console.error('Error loading regions:', error);
    }
}

function populateRegionDropdowns(regions) {
    const dropdowns = ['climate_region', 'agri_region', 'sensor_region'];
    
    dropdowns.forEach(dropdownId => {
        const dropdown = document.getElementById(dropdownId);
        dropdown.innerHTML = '<option value="">Select a region</option>';
        
        regions.forEach(region => {
            const option = document.createElement('option');
            option.value = region.region_id;
            option.textContent = region.region_name;
            dropdown.appendChild(option);
        });
    });
}

function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab
    document.getElementById(`${tabName}Tab`).classList.add('active');
    event.target.classList.add('active');
}

// Climate Data Form
document.getElementById('climateForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const messageDiv = document.getElementById('climateMessage');
    messageDiv.textContent = '';
    messageDiv.className = 'message';
    
    const data = {
        region_id: parseInt(document.getElementById('climate_region').value),
        temperature: parseFloat(document.getElementById('temperature').value),
        rainfall: parseFloat(document.getElementById('rainfall').value),
        humidity: parseFloat(document.getElementById('humidity').value)
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/insert-climate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            messageDiv.textContent = 'Climate data inserted successfully!';
            messageDiv.className = 'message success';
            document.getElementById('climateForm').reset();
        } else {
            messageDiv.textContent = result.error || 'Failed to insert data';
            messageDiv.className = 'message error';
        }
    } catch (error) {
        messageDiv.textContent = 'Connection error';
        messageDiv.className = 'message error';
        console.error('Insert error:', error);
    }
});

// Agriculture Data Form
document.getElementById('agricultureForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const messageDiv = document.getElementById('agricultureMessage');
    messageDiv.textContent = '';
    messageDiv.className = 'message';
    
    const data = {
        region_id: parseInt(document.getElementById('agri_region').value),
        crop_type: document.getElementById('crop_type').value,
        yield: parseFloat(document.getElementById('yield').value),
        season: document.getElementById('season').value,
        year: parseInt(document.getElementById('year').value)
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/insert-agriculture`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            messageDiv.textContent = 'Agriculture data inserted successfully!';
            messageDiv.className = 'message success';
            document.getElementById('agricultureForm').reset();
        } else {
            messageDiv.textContent = result.error || 'Failed to insert data';
            messageDiv.className = 'message error';
        }
    } catch (error) {
        messageDiv.textContent = 'Connection error';
        messageDiv.className = 'message error';
        console.error('Insert error:', error);
    }
});

// Sensor Log Form
document.getElementById('sensorForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const messageDiv = document.getElementById('sensorMessage');
    messageDiv.textContent = '';
    messageDiv.className = 'message';
    
    const data = {
        sensor_id: document.getElementById('sensor_id').value,
        region_id: parseInt(document.getElementById('sensor_region').value),
        event_type: document.getElementById('event_type').value,
        severity: document.getElementById('severity').value,
        message: document.getElementById('message').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/insert-sensor-log`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            messageDiv.textContent = 'Sensor log inserted successfully!';
            messageDiv.className = 'message success';
            document.getElementById('sensorForm').reset();
        } else {
            messageDiv.textContent = result.error || 'Failed to insert data';
            messageDiv.className = 'message error';
        }
    } catch (error) {
        messageDiv.textContent = 'Connection error';
        messageDiv.className = 'message error';
        console.error('Insert error:', error);
    }
});

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
