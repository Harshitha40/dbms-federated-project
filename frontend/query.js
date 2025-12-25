// ========================================
// Federated Query Interface JavaScript
// ========================================

const API_BASE_URL = '';
let currentUserRole = null;
let lastQueryResult = null;
let lastQueryColumns = null;
let currentChart = null;

window.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    await loadSampleQueries();
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
            currentUserRole = data.user.role;
            if (currentUserRole === 'Data Provider') {
                alert('Access denied: Federated Query interface is restricted for Data Providers.');
                window.location.href = 'dashboard.html';
            }
        }
    } catch (error) {
        console.error('Auth check error:', error);
        window.location.href = 'login.html';
    }
}

async function loadSampleQueries() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/sample-queries`, {
            credentials: 'include'
        });

        const data = await response.json();

        if (data.success) {
            displaySampleQueries(data.queries);
        }
    } catch (error) {
        console.error('Error loading sample queries:', error);
    }
}

function displaySampleQueries(queries) {
    const container = document.getElementById('sampleQueriesList');
    container.innerHTML = '';

    queries.forEach(query => {
        const queryCard = document.createElement('div');
        queryCard.className = 'sample-query-card';
        queryCard.innerHTML = `
            <h4>${query.name}</h4>
            <p>${query.description}</p>
            <button onclick="useSampleQuery(\`${query.query.replace(/`/g, '\\`')}\`)" class="btn btn-small">Use This Query</button>
        `;
        container.appendChild(queryCard);
    });
}

function useSampleQuery(query) {
    document.getElementById('queryInput').value = query;
}

async function executeQuery() {
    const queryInput = document.getElementById('queryInput').value.trim();
    const messageDiv = document.getElementById('queryMessage');
    const resultsArea = document.getElementById('resultsArea');

    // Clear previous messages
    messageDiv.textContent = '';
    messageDiv.className = 'message';

    if (!queryInput) {
        messageDiv.textContent = 'Please enter a query';
        messageDiv.className = 'message error';
        return;
    }

    // Show loading
    resultsArea.innerHTML = '<p class="loading">Executing query...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/federated-query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ query: queryInput })
        });

        const data = await response.json();

        if (data.success) {
            messageDiv.textContent = `Query executed successfully! (${data.data.length} rows)`;
            messageDiv.className = 'message success';
            displayResults(data.data, data.columns);
        } else {
            messageDiv.textContent = data.error || 'Query execution failed';
            messageDiv.className = 'message error';
            resultsArea.innerHTML = '<p class="error">Query failed. Check your syntax and try again.</p>';
        }
    } catch (error) {
        messageDiv.textContent = 'Connection error. Please ensure Apache Drill is running.';
        messageDiv.className = 'message error';
        resultsArea.innerHTML = '<p class="error">Failed to execute query</p>';
        console.error('Query error:', error);
    }
}

function displayResults(data, columns) {
    const resultsArea = document.getElementById('resultsArea');
    const vizSection = document.getElementById('vizSection');

    // Store data for visualization
    lastQueryResult = data;
    lastQueryColumns = columns;

    if (!data || data.length === 0) {
        resultsArea.innerHTML = '<p class="info">Query returned no results</p>';
        if (vizSection) vizSection.style.display = 'none';
        return;
    }

    // Show visualization section only for Researchers
    if (vizSection && currentUserRole === 'Researcher') {
        vizSection.style.display = 'block';
        populateAxisSelectors(columns);
    } else if (vizSection) {
        vizSection.style.display = 'none';
    }

    // Get column names from first row
    const columnNames = Object.keys(data[0]);

    // Build HTML table
    let tableHTML = '<div class="table-container"><table class="data-table"><thead><tr>';

    // Table header
    columnNames.forEach(col => {
        tableHTML += `<th>${col}</th>`;
    });
    tableHTML += '</tr></thead>';

    // Table body
    tableHTML += '<tbody>';
    data.forEach(row => {
        tableHTML += '<tr>';
        columnNames.forEach(col => {
            let value = row[col];
            // Format value
            if (value === null || value === undefined) {
                value = '<span class="null-value">NULL</span>';
            } else if (Array.isArray(value)) {
                // Join array elements with commas and spaces
                value = value.join(', ');
            } else if (typeof value === 'object') {
                value = JSON.stringify(value);
            }
            tableHTML += `<td>${value}</td>`;
        });
        tableHTML += '</tr>';
    });
    tableHTML += '</tbody></table></div>';

    resultsArea.innerHTML = tableHTML;
}

function clearQuery() {
    document.getElementById('queryInput').value = '';
    document.getElementById('queryMessage').textContent = '';
    document.getElementById('queryMessage').className = 'message';
    document.getElementById('resultsArea').innerHTML = '<p class="placeholder">Execute a query to see results here</p>';
}

async function executeNaturalQuery() {
    const naturalInput = document.getElementById('naturalQueryInput').value.trim();
    const messageDiv = document.getElementById('naturalMessage');
    const resultsArea = document.getElementById('resultsArea');
    const infoBox = document.getElementById('naturalQueryInfo');

    // Clear previous messages
    messageDiv.textContent = '';
    messageDiv.className = 'message';

    if (!naturalInput) {
        messageDiv.textContent = 'Please enter a question';
        messageDiv.className = 'message error';
        return;
    }

    // Show loading
    resultsArea.innerHTML = '<p class="loading">🤖 Processing your question...</p>';
    infoBox.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE_URL}/api/natural-query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ query: naturalInput })
        });

        const data = await response.json();

        console.log('=== Natural Query Response ===');
        console.log('Success:', data.success);
        console.log('Data length:', data.data ? data.data.length : 'undefined');
        console.log('Generated SQL:', data.generated_sql);
        console.log('Full response:', data);
        console.log('============================');

        if (data.success) {
            // Show interpretation info
            document.getElementById('interpretation').textContent = data.interpretation;
            document.getElementById('confidence').textContent = (data.confidence * 100).toFixed(0) + '%';
            document.getElementById('generatedSQL').textContent = data.generated_sql;
            infoBox.style.display = 'block';

            messageDiv.textContent = `✓ Question answered! (${data.data.length} results, ${(data.confidence * 100).toFixed(0)}% confidence)`;
            messageDiv.className = 'message success';
            displayResults(data.data, data.columns);
        } else {
            messageDiv.textContent = data.error || 'Failed to process question';
            messageDiv.className = 'message error';
            resultsArea.innerHTML = '<p class="error">Could not answer your question. Try rephrasing it.</p>';

            // Still show what was generated
            if (data.generated_sql) {
                document.getElementById('interpretation').textContent = data.interpretation || 'N/A';
                document.getElementById('confidence').textContent = data.confidence ? (data.confidence * 100).toFixed(0) + '%' : 'N/A';
                document.getElementById('generatedSQL').textContent = data.generated_sql;
                infoBox.style.display = 'block';
            }
        }
    } catch (error) {
        messageDiv.textContent = 'Connection error. Please ensure the server is running.';
        messageDiv.className = 'message error';
        resultsArea.innerHTML = '<p class="error">Failed to process question</p>';
        console.error('Natural query error:', error);
    }
}

function clearNaturalQuery() {
    document.getElementById('naturalQueryInput').value = '';
    document.getElementById('naturalMessage').textContent = '';
    document.getElementById('naturalMessage').className = 'message';
    document.getElementById('naturalQueryInfo').style.display = 'none';
    document.getElementById('resultsArea').innerHTML = '<p class="placeholder">Execute a query to see results here</p>';
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

// --- VISUALIZATION FUNCTIONS ---

function populateAxisSelectors(columns) {
    const xSelect = document.getElementById('xAxisSelect');
    const ySelect = document.getElementById('yAxisSelect');

    if (!xSelect || !ySelect) return;

    xSelect.innerHTML = '';
    ySelect.innerHTML = '';

    columns.forEach(col => {
        const xOpt = document.createElement('option');
        xOpt.value = col;
        xOpt.textContent = col;
        xSelect.appendChild(xOpt);

        const yOpt = document.createElement('option');
        yOpt.value = col;
        yOpt.textContent = col;
        ySelect.appendChild(yOpt);
    });
}

function generateChart() {
    const xAxis = document.getElementById('xAxisSelect').value;
    const yAxis = document.getElementById('yAxisSelect').value;
    const type = document.getElementById('chartTypeSelect').value;
    const ctx = document.getElementById('dataChart').getContext('2d');

    if (!lastQueryResult || !xAxis || !yAxis) return;

    // Process labels and data
    const labels = lastQueryResult.map(row => row[xAxis] || 'Unknown');
    const values = lastQueryResult.map(row => {
        const val = row[yAxis];
        const parsed = parseFloat(val);
        return isNaN(parsed) ? 0 : parsed;
    });

    // Destroy existing chart if any
    if (currentChart) {
        currentChart.destroy();
    }

    // Generate distinct colors for Pie charts
    const backgroundColors = lastQueryResult.map((_, i) => `hsl(${(i * 360) / lastQueryResult.length}, 70%, 50%)`);

    currentChart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: `${yAxis} vs ${xAxis}`,
                data: values,
                backgroundColor: type === 'pie' ? backgroundColors : 'rgba(0, 204, 102, 0.2)',
                borderColor: 'rgba(0, 204, 102, 1)',
                borderWidth: 1,
                fill: type === 'line'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: type === 'pie' ? {} : {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: type === 'pie'
                }
            }
        }
    });
}
