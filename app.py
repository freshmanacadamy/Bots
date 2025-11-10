from flask import Flask, jsonify
import time
import psutil
import os
from datetime import datetime

app = Flask(__name__)

# Store bot start time
start_time = time.time()
request_count = 0

@app.route('/')
def home():
    global request_count
    request_count += 1
    
    uptime_seconds = time.time() - start_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    
    memory = psutil.Process().memory_info()
    
    return jsonify({
        'message': '🤖 24/7 Python Bot is running!',
        'status': 'online',
        'uptime': f'{hours}h {minutes}m {seconds}s',
        'total_requests': request_count,
        'memory_used': f'{memory.rss / 1024 / 1024:.2f} MB',
        'start_time': datetime.fromtimestamp(start_time).isoformat(),
        'python_version': os.environ.get('PYTHON_VERSION', '3.9+')
    })

@app.route('/health')
def health():
    """Health check endpoint for Uptime Robot"""
    uptime = time.time() - start_time
    memory = psutil.virtual_memory()
    
    # Health checks
    is_healthy = uptime > 0 and memory.percent < 90
    
    status_code = 200 if is_healthy else 500
    
    return jsonify({
        'status': 'healthy' if is_healthy else 'degraded',
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': int(uptime),
        'memory_usage': f'{memory.percent}%',
        'server': 'Flask Python'
    }), status_code

@app.route('/activity')
def activity():
    """Simulate bot activity"""
    print(f"✅ Activity ping at {datetime.now().isoformat()}")
    
    return jsonify({
        'activity': 'simulated_task',
        'executed_at': datetime.now().isoformat(),
        'result': 'Python task completed successfully',
        'server': 'Flask'
    })

@app.route('/api/users')
def api_users():
    """Example API endpoint"""
    users = [
        {'id': 1, 'name': 'Alice', 'status': 'active', 'language': 'Python'},
        {'id': 2, 'name': 'Bob', 'status': 'inactive', 'language': 'Python'},
        {'id': 3, 'name': 'Charlie', 'status': 'active', 'language': 'Python'}
    ]
    return jsonify(users)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Route not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"""
🚀 24/7 Python Bot Started Successfully!
📍 Port: {port}
⏰ Start Time: {datetime.now().isoformat()}
📊 Python: {os.environ.get('PYTHON_VERSION', '3.9+')}
🔗 Local: http://localhost:{port}
🔗 Health: http://localhost:{port}/health
    """)
    
    app.run(host='0.0.0.0', port=port, debug=False)