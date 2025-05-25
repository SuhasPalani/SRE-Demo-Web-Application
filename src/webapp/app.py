#!/usr/bin/env python3
"""
Simple Flask web application for SRE monitoring demo
"""

from flask import Flask, jsonify, render_template
import time
import random
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulate application state
app_state = {
    'status': 'healthy',
    'start_time': time.time(),
    'request_count': 0,
    'error_count': 0
}

@app.route('/')
def home():
    """Serve the UI page"""
    app_state['request_count'] += 1
    return render_template('index.html', uptime=time.time() - app_state['start_time'], status=app_state['status'])

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    app_state['request_count'] += 1

    # Simulate occasional health issues
    if random.random() < 0.05:  # 5% chance of failure
        app_state['status'] = 'degraded'
        app_state['error_count'] += 1
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': 'Simulated service degradation'
        }), 503

    app_state['status'] = 'healthy'
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': time.time() - app_state['start_time'],
        'memory_usage': get_memory_usage()
    })

@app.route('/metrics')
def metrics():
    """Metrics endpoint returning JSON format"""
    app_state['request_count'] += 1

    # Gather metrics in a dictionary
    metrics_data = {
        "app_requests_total": app_state['request_count'],
        "app_errors_total": app_state['error_count'],
        "app_uptime_seconds": time.time() - app_state['start_time']
    }

    return jsonify(metrics_data)

@app.route('/crash')
def simulate_crash():
    """Endpoint to simulate application crash"""
    logger.error("Simulated crash triggered!")
    app_state['error_count'] += 1
    os._exit(1)

def get_memory_usage():
    """Get current memory usage"""
    try:
        import psutil
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # MB
    except ImportError:
        logger.warning("psutil module not found. Memory usage won't be available.")
        return 0

if __name__ == '__main__':
    logger.info("Starting SRE Demo Application")
    app.run(host='0.0.0.0', port=5000, debug=False)
