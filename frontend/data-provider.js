// ========================================
// Data Provider Interface JavaScript
// ========================================

const API_BASE_URL = '';

window.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await loadRegions();

    // Handle URL parameters for tab switching
    const urlParams = new URLSearchParams(window.location.search);
    const tab = urlParams.get('tab');
    if (tab) {
        showTab(tab);
    }
});

async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/current-user`, {
            credentials: 'include'
        });

        const data = await response.json();
        if (data.success) {
            const currentUser = data.user;
            // Hide restricted navigation items for Data Provider
            if (currentUser.role === 'Data Provider') {
                const navQuery = document.getElementById('navQuery');
                const navAdmin = document.getElementById('navAdmin');
                if (navQuery) navQuery.style.display = 'none';
                if (navAdmin) navAdmin.style.display = 'none';
            }
        } else {
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
    const dropdowns = document.querySelectorAll('.region-select');

    dropdowns.forEach(dropdown => {
        dropdown.innerHTML = '<option value="" disabled selected>Select Region...</option>';

        regions.forEach(region => {
            const option = document.createElement('option');
            option.value = region.region_id;
            option.textContent = region.region_name;
            dropdown.appendChild(option);
        });
    });
}

function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    const targetTab = document.getElementById(`${tabName}Tab`);
    if (targetTab) {
        targetTab.classList.add('active');
        // Sync the dropdown if it's not already set (for URL param case)
        const selector = document.getElementById('tableSelector');
        if (selector) {
            selector.value = tabName;
        }
    }
}

// Utility for form submission
async function handleFormSubmit(formId, endpoint, messageId, dataMapper) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const messageDiv = document.getElementById(messageId);
        messageDiv.textContent = 'Processing...';
        messageDiv.className = 'message';
        messageDiv.style.display = 'block';

        const data = dataMapper();

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify(data)
            });

            const result = await response.json();
            if (result.success) {
                messageDiv.textContent = 'Success: Record inserted successfully!';
                messageDiv.className = 'message success';
                form.reset();
            } else {
                messageDiv.textContent = 'Error: ' + (result.error || 'Failed to insert');
                messageDiv.className = 'message error';
            }
        } catch (error) {
            messageDiv.textContent = 'Connection error';
            messageDiv.className = 'message error';
            console.error('Insert error:', error);
        }
    });
}

// Register all forms
handleFormSubmit('climateForm', '/api/insert-climate', 'climateMessage', () => ({
    region_id: parseInt(document.getElementById('climate_region').value),
    temperature: parseFloat(document.getElementById('temperature').value),
    rainfall: parseFloat(document.getElementById('rainfall').value),
    humidity: parseFloat(document.getElementById('humidity').value)
}));

handleFormSubmit('agricultureForm', '/api/insert-agriculture', 'agricultureMessage', () => ({
    region_id: parseInt(document.getElementById('agri_region').value),
    crop_type: document.getElementById('crop_type').value,
    yield: parseFloat(document.getElementById('yield').value),
    season: document.getElementById('season').value,
    year: parseInt(document.getElementById('year').value)
}));

handleFormSubmit('regionForm', '/api/insert-region', 'regionMessage', () => ({
    region_name: document.getElementById('region_name').value,
    latitude: parseFloat(document.getElementById('latitude').value),
    longitude: parseFloat(document.getElementById('longitude').value)
}));

handleFormSubmit('sensorForm', '/api/insert-sensor-log', 'sensorMessage', () => ({
    sensor_id: document.getElementById('sensor_id').value,
    region_id: parseInt(document.getElementById('sensor_region').value),
    event_type: document.getElementById('event_type').value,
    severity: document.getElementById('severity').value,
    message: document.getElementById('message').value
}));

handleFormSubmit('biodiversityForm', '/api/insert-biodiversity', 'biodiversityMessage', () => ({
    biodiversity_id: document.getElementById('bio_id').value,
    region_id: parseInt(document.getElementById('bio_region').value),
    species_count: parseInt(document.getElementById('bio_species_count').value),
    endangered_species: document.getElementById('bio_endangered').value,
    dominant_flora: document.getElementById('bio_flora').value,
    conservation_status: document.getElementById('bio_status').value
}));

handleFormSubmit('air_qualityForm', '/api/insert-air-quality', 'air_qualityMessage', () => ({
    reading_id: document.getElementById('aq_id').value,
    region_id: parseInt(document.getElementById('aq_region').value),
    aqi: parseInt(document.getElementById('aq_aqi').value),
    co2: parseFloat(document.getElementById('aq_co2').value),
    pm2_5: parseFloat(document.getElementById('aq_pm25').value),
    pm10: parseFloat(document.getElementById('aq_pm10').value),
    no2: parseFloat(document.getElementById('aq_no2').value),
    so2: parseFloat(document.getElementById('aq_so2').value),
    o3: parseFloat(document.getElementById('aq_o3').value),
    air_quality_level: document.getElementById('aq_status').value
}));

handleFormSubmit('speciesForm', '/api/insert-species', 'speciesMessage', () => ({
    species_id: document.getElementById('sp_id').value,
    common_name: document.getElementById('sp_common').value,
    scientific_name: document.getElementById('sp_scientific').value,
    habitat_regions: document.getElementById('sp_habitat').value,
    population_estimate: parseInt(document.getElementById('sp_pop').value),
    lifespan_years: parseInt(document.getElementById('sp_lifespan').value),
    diet: document.getElementById('diet').value,
    conservation_status: document.getElementById('sp_status').value
}));

handleFormSubmit('sensor_metadataForm', '/api/insert-sensor-metadata', 'sensor_metadataMessage', () => ({
    sensor_id: document.getElementById('sm_id').value,
    sensor_type: document.getElementById('sm_type').value,
    region_id: parseInt(document.getElementById('sm_region').value),
    manufacturer: document.getElementById('sm_manu').value,
    model: document.getElementById('sm_model').value,
    accuracy_rating: parseFloat(document.getElementById('sm_accuracy').value),
    measurements: document.getElementById('sm_measurements').value,
    status: 'active'
}));

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
