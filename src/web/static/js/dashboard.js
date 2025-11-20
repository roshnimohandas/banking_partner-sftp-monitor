// Dashboard JavaScript

// Initialize Socket.IO
const socket = io();

// State
let activeConnections = new Set();
let currentMonitoringConnection = null;

// Socket event handlers
socket.on('connect', () => {
    console.log('Connected to server');
    updateConnectionStatus(true);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    updateConnectionStatus(false);
});

socket.on('file_alert', (data) => {
    console.log('Received alert:', data);
    addAlert(data);
    showNotification('File Alert', `Invalid file detected: ${data.file}`, 'error');
});

// Update connection status badge
function updateConnectionStatus(connected) {
    const statusBadge = document.getElementById('connection-status');
    if (connected) {
        statusBadge.textContent = 'Connected';
        statusBadge.classList.add('connected');
    } else {
        statusBadge.textContent = 'Disconnected';
        statusBadge.classList.remove('connected');
    }
}

// Connection form handler
document.getElementById('connection-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        connection_name: document.getElementById('connection-name').value,
        host: document.getElementById('host').value,
        port: parseInt(document.getElementById('port').value),
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch('/api/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.success) {
            activeConnections.add(formData.connection_name);
            updateConnectionSelect();
            showNotification('Success', `Connected to ${formData.host}`, 'success');

            // Reset form
            document.getElementById('connection-form').reset();
        } else {
            showNotification('Error', result.error || 'Failed to connect', 'error');
        }
    } catch (error) {
        console.error('Connection error:', error);
        showNotification('Error', 'Failed to connect to server', 'error');
    }
});

// Monitor form handler
document.getElementById('monitor-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        remote_path: document.getElementById('remote-path').value,
        partner: document.getElementById('partner').value
    };

    const connectionName = document.getElementById('monitor-connection').value;

    if (!connectionName) {
        showNotification('Error', 'Please select a connection', 'error');
        return;
    }

    try {
        const response = await fetch(`/api/monitor/${connectionName}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.success) {
            currentMonitoringConnection = connectionName;
            displayMonitoringResults(result);
            showNotification('Success', 'Files monitored successfully', 'success');
        } else {
            showNotification('Error', result.error || 'Failed to monitor files', 'error');
        }
    } catch (error) {
        console.error('Monitoring error:', error);
        showNotification('Error', 'Failed to monitor files', 'error');
    }
});

// Update connection select dropdown
function updateConnectionSelect() {
    const select = document.getElementById('monitor-connection');
    select.innerHTML = '<option value="">Select connection...</option>';

    activeConnections.forEach(conn => {
        const option = document.createElement('option');
        option.value = conn;
        option.textContent = conn;
        select.appendChild(option);
    });
}

// Display monitoring results
function displayMonitoringResults(result) {
    // Show results section
    document.getElementById('monitoring-results').style.display = 'block';

    // Update summary stats
    document.getElementById('total-files').textContent = result.summary.total_files;
    document.getElementById('valid-files').textContent = result.summary.valid_files;
    document.getElementById('invalid-files').textContent = result.summary.invalid_files;

    // Update last check time
    const lastCheck = new Date(result.last_check);
    document.getElementById('last-check').textContent = `Last check: ${lastCheck.toLocaleTimeString()}`;

    // Display files in table
    displayFilesTable(result.files);
}

// Display files in table
function displayFilesTable(files) {
    const tbody = document.getElementById('files-tbody');

    if (files.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="no-data">No files found</td></tr>';
        return;
    }

    tbody.innerHTML = '';

    files.forEach(file => {
        const row = document.createElement('tr');

        // Status icon
        const statusCell = document.createElement('td');
        statusCell.innerHTML = file.valid
            ? '<span class="status-icon">✅</span>'
            : '<span class="status-icon">❌</span>';
        row.appendChild(statusCell);

        // Filename
        const nameCell = document.createElement('td');
        nameCell.textContent = file.filename;
        row.appendChild(nameCell);

        // Size
        const sizeCell = document.createElement('td');
        sizeCell.textContent = formatBytes(file.size);
        row.appendChild(sizeCell);

        // Modified
        const modifiedCell = document.createElement('td');
        const modDate = new Date(file.modified);
        modifiedCell.textContent = modDate.toLocaleString();
        row.appendChild(modifiedCell);

        // Validation
        const validationCell = document.createElement('td');
        if (file.valid) {
            validationCell.innerHTML = '<span style="color: #4caf50;">Valid</span>';
        } else {
            const errors = file.errors.join(', ');
            validationCell.innerHTML = `<span style="color: #f44336;" title="${errors}">Invalid</span>`;
        }
        row.appendChild(validationCell);

        tbody.appendChild(row);
    });
}

// Add alert to alerts panel
function addAlert(alert) {
    const container = document.getElementById('alerts-container');

    // Remove "no alerts" message
    if (container.querySelector('.no-data')) {
        container.innerHTML = '';
    }

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert-item ${alert.severity}`;

    const header = document.createElement('div');
    header.className = 'alert-header';

    const title = document.createElement('span');
    title.textContent = `${alert.connection}: ${alert.file}`;
    header.appendChild(title);

    const timestamp = document.createElement('span');
    timestamp.className = 'alert-timestamp';
    const alertTime = new Date(alert.timestamp);
    timestamp.textContent = alertTime.toLocaleTimeString();
    header.appendChild(timestamp);

    alertDiv.appendChild(header);

    if (alert.errors && alert.errors.length > 0) {
        const errorsDiv = document.createElement('div');
        errorsDiv.className = 'alert-errors';

        const errorList = document.createElement('ul');
        alert.errors.forEach(error => {
            const li = document.createElement('li');
            li.textContent = error;
            errorList.appendChild(li);
        });

        errorsDiv.appendChild(errorList);
        alertDiv.appendChild(errorsDiv);
    }

    // Add to top of container
    container.insertBefore(alertDiv, container.firstChild);

    // Limit to 10 alerts
    while (container.children.length > 10) {
        container.removeChild(container.lastChild);
    }
}

// Show notification
function showNotification(title, message, type) {
    // Simple console notification for now
    // In production, use a proper notification library
    console.log(`[${type.toUpperCase()}] ${title}: ${message}`);

    // Could integrate with browser notifications API
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, {
            body: message,
            icon: type === 'error' ? '❌' : '✅'
        });
    }
}

// Format bytes to human readable
function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Load status on page load
async function loadStatus() {
    try {
        const response = await fetch('/api/status');
        const status = await response.json();

        // Update active connections
        if (status.active_connections) {
            Object.keys(status.active_connections).forEach(conn => {
                activeConnections.add(conn);
            });
            updateConnectionSelect();
        }

        // Update last check
        if (status.last_check) {
            const lastCheck = new Date(status.last_check);
            document.getElementById('last-check').textContent = `Last check: ${lastCheck.toLocaleTimeString()}`;
        }
    } catch (error) {
        console.error('Failed to load status:', error);
    }
}

// Load alerts
async function loadAlerts() {
    try {
        const response = await fetch('/api/alerts?limit=10');
        const data = await response.json();

        if (data.alerts && data.alerts.length > 0) {
            data.alerts.forEach(alert => addAlert(alert));
        }
    } catch (error) {
        console.error('Failed to load alerts:', error);
    }
}

// Request notification permission
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStatus();
    loadAlerts();

    // Auto-refresh every 30 seconds if monitoring
    setInterval(() => {
        if (currentMonitoringConnection) {
            document.getElementById('monitor-form').dispatchEvent(new Event('submit'));
        }
    }, 30000);
});
