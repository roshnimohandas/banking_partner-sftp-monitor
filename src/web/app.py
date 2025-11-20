"""
Web interface for SFTP file monitoring dashboard
Free version using Flask
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.validators.sftp_client import SFTPClient
from src.validators.file_validator import FileValidator

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('WEB_SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store monitoring status
monitoring_status = {
    'active_connections': {},
    'last_check': None,
    'alerts': []
}


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/config')
def get_config():
    """Get configuration for banking partners"""
    config_path = Path(__file__).parent.parent.parent / 'config' / 'partners.json'

    if not config_path.exists():
        return jsonify({'error': 'Configuration file not found'}), 404

    with open(config_path, 'r') as f:
        config = json.load(f)

    return jsonify(config)


@app.route('/api/connect', methods=['POST'])
def connect_sftp():
    """Connect to SFTP server"""
    data = request.json

    required_fields = ['connection_name', 'host', 'username']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        client = SFTPClient(
            host=data['host'],
            port=data.get('port', 22),
            username=data['username'],
            password=data.get('password'),
            private_key_path=data.get('private_key_path')
        )

        if client.connect():
            connection_name = data['connection_name']
            monitoring_status['active_connections'][connection_name] = {
                'client': client,
                'host': data['host'],
                'connected_at': datetime.now().isoformat()
            }

            return jsonify({
                'success': True,
                'message': f'Connected to {data["host"]}',
                'connection_name': connection_name
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to connect to SFTP server'
            }), 500

    except Exception as e:
        logger.error(f"Error connecting to SFTP: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/monitor/<connection_name>', methods=['POST'])
def monitor_files(connection_name):
    """Monitor files in SFTP directory"""
    if connection_name not in monitoring_status['active_connections']:
        return jsonify({'error': 'Connection not found'}), 404

    data = request.json
    remote_path = data.get('remote_path', '.')
    partner = data.get('partner', 'GENERIC')

    try:
        client = monitoring_status['active_connections'][connection_name]['client']

        # List files
        files = client.list_files(remote_path)

        # Filter only files (not directories)
        files = [f for f in files if not f['is_dir']]

        # Validate each file
        validator = FileValidator(partner)
        validated_files = []

        for file_info in files:
            validation_result = validator.validate_all(
                filename=file_info['filename'],
                file_size=file_info['size'],
                file_mtime=file_info['mtime']
            )

            validated_files.append({
                'filename': file_info['filename'],
                'size': file_info['size'],
                'modified': file_info['modified_date'],
                'valid': validation_result['valid'],
                'errors': validation_result['errors'],
                'warnings': validation_result['warnings']
            })

        # Update last check time
        monitoring_status['last_check'] = datetime.now().isoformat()

        # Create alerts for invalid files
        for file in validated_files:
            if not file['valid']:
                alert = {
                    'timestamp': datetime.now().isoformat(),
                    'severity': 'error',
                    'connection': connection_name,
                    'file': file['filename'],
                    'errors': file['errors']
                }
                monitoring_status['alerts'].append(alert)

                # Emit socket event
                socketio.emit('file_alert', alert)

        # Summary
        total_files = len(validated_files)
        valid_files = sum(1 for f in validated_files if f['valid'])
        invalid_files = total_files - valid_files

        result = {
            'success': True,
            'connection': connection_name,
            'path': remote_path,
            'partner': partner,
            'summary': {
                'total_files': total_files,
                'valid_files': valid_files,
                'invalid_files': invalid_files
            },
            'files': validated_files,
            'last_check': monitoring_status['last_check']
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error monitoring files: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts"""
    limit = request.args.get('limit', 50, type=int)
    severity = request.args.get('severity')

    alerts = monitoring_status['alerts']

    # Filter by severity if specified
    if severity:
        alerts = [a for a in alerts if a['severity'] == severity]

    # Return most recent alerts
    recent_alerts = alerts[-limit:]

    return jsonify({
        'alerts': recent_alerts,
        'total': len(monitoring_status['alerts'])
    })


@app.route('/api/status')
def get_status():
    """Get monitoring status"""
    connections = {}
    for name, conn in monitoring_status['active_connections'].items():
        connections[name] = {
            'host': conn['host'],
            'connected_at': conn['connected_at']
        }

    return jsonify({
        'active_connections': connections,
        'last_check': monitoring_status['last_check'],
        'alert_count': len(monitoring_status['alerts'])
    })


@app.route('/api/validate/<connection_name>', methods=['POST'])
def validate_file(connection_name):
    """Validate a specific file"""
    if connection_name not in monitoring_status['active_connections']:
        return jsonify({'error': 'Connection not found'}), 404

    data = request.json
    remote_path = data.get('remote_path')
    partner = data.get('partner', 'GENERIC')

    if not remote_path:
        return jsonify({'error': 'remote_path is required'}), 400

    try:
        client = monitoring_status['active_connections'][connection_name]['client']

        # Get file metadata
        metadata = client.get_file_metadata(remote_path)

        if not metadata:
            return jsonify({'error': 'File not found'}), 404

        # Extract filename from path
        filename = os.path.basename(remote_path)

        # Validate file
        validator = FileValidator(partner)
        validation_result = validator.validate_all(
            filename=filename,
            file_size=metadata['size'],
            file_mtime=metadata['mtime']
        )

        result = {
            'success': True,
            'path': remote_path,
            'validation': validation_result
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error validating file: {str(e)}")
        return jsonify({'error': str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    logger.info('Client connected')
    emit('status', {'message': 'Connected to monitoring server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    logger.info('Client disconnected')


if __name__ == '__main__':
    host = os.getenv('WEB_HOST', '0.0.0.0')
    port = int(os.getenv('WEB_PORT', 5000))

    logger.info(f"Starting web server on {host}:{port}")
    socketio.run(app, host=host, port=port, debug=True)
