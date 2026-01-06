from flask import Flask, render_template, jsonify
import sqlite3
import os
import sys

# Añadir root al path para importar core
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.database import db

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def api_stats():
    """Devuelve estadísticas generales"""
    stats = db.get_stats()
    workers = db.get_workers() 
    return jsonify({"stats": stats, "workers": workers})

@app.route('/api/runs')
def api_runs():
    """Devuelve últimas ejecuciones"""
    runs = db.get_runs(limit=10)
    return jsonify(runs)

@app.route('/api/logs')
def api_logs():
    """Devuelve últimos logs"""
    logs = db.get_logs(limit=20)
    return jsonify(logs)

def start_dashboard(host='0.0.0.0', port=5000):
    print(f"🌍 Dashboard iniciado en http://{host}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)

if __name__ == '__main__':
    start_dashboard()
