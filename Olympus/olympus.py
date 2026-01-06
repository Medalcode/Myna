#!/usr/bin/env python3
"""
Olympus V4.0 - Orquestador Principal
Gestiona todos los workers y el dashboard
"""

import os
import sys
import time
import signal
import threading
from datetime import datetime

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.database import db
from workers.hermes import HermesWorker
from dashboard import start_dashboard

class Olympus:
    def __init__(self):
        self.running = True
        self.workers = []
        
        print("🏛️  OLYMPUS V4.0 - Sistema de Orquestación")
        print("=" * 60)
        
        # Inicializar DB
        db._ensure_db()
        db.log("Olympus iniciado", "INFO", "olympus")
        
        # Registrar workers
        self.workers.append(HermesWorker())
        
    def start(self):
        """Inicia Olympus y todos sus componentes"""
        print("\n🚀 Iniciando Olympus...")
        
        # Iniciar Dashboard en hilo separado
        print("   Iniciando Dashboard Web (Puerto 5000)...")
        dash_thread = threading.Thread(target=start_dashboard, kwargs={'port': 5000}, daemon=True)
        dash_thread.start()
        
        # Iniciar workers
        for worker in self.workers:
            print(f"   Iniciando worker: {worker.name}")
            worker.start()
            time.sleep(1) # Pequeña pausa entre inicios
        
        print("✅ Olympus iniciado correctamente")
        print("\nPresiona Ctrl+C para detener")
        
        try:
            while self.running:
                # Watchdog loop simple
                time.sleep(10)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Detiene Olympus y todos sus workers"""
        print("\n\n🛑 Deteniendo Olympus...")
        self.running = False
        
        for worker in self.workers:
            print(f"   Deteniendo worker: {worker.name}")
            worker.stop()
            
        db.log("Olympus detenido", "INFO", "olympus")
        print("✅ Olympus detenido correctamente")

if __name__ == "__main__":
    olympus = Olympus()
    olympus.start()
