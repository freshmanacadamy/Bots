from flask import Flask, jsonify
import os
import time
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
    
    return jsonify({
        'message': '🤖 24/7 Python Bot is running!',
        'status': 'online',
        'uptime': f'{hours}h {minutes}m {seconds}s',
        'total_requests': request_count,
        'start_time': datetime.fromtimestamp(start_time).isoformat(),
        'python_version': '3.9+'
    })

@app.route('/health')
def health():
    """Health check endpoint for Uptime Robot"""
    uptime = time.time() - start_time
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': int(uptime),
        'server': 'Flask Python'
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"🚀 Bot started on port {port}")
    app.run(host='0.0.0.0', port=port)
