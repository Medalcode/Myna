"""
Base Worker Class
Todos los workers heredan de esta clase
"""
import os
import sys
import time
import threading
from abc import ABC, abstractmethod
from datetime import datetime

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import db

class BaseWorker(ABC):
    """Clase base para todos los workers de Olympus"""
    
    def __init__(self, name: str):
        self.name = name
        self.running = False
        self.thread = None
        self.pid = os.getpid()
        
    def start(self):
        """Inicia el worker en un thread separado"""
        if self.running:
            print(f"⚠️  {self.name} ya está corriendo")
            return
        
        self.running = True
        db.register_worker(self.name, self.pid)
        db.log(f"{self.name} iniciado", "INFO", self.name)
        
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        print(f"✅ {self.name} iniciado")
    
    def stop(self):
        """Detiene el worker"""
        if not self.running:
            return
        
        self.running = False
        db.log(f"{self.name} detenido", "INFO", self.name)
        print(f"🛑 {self.name} detenido")
    
    def _run_loop(self):
        """Loop principal del worker"""
        while self.running:
            try:
                self.work()
                time.sleep(self.get_sleep_time())
            except Exception as e:
                db.log(f"Error en {self.name}: {str(e)}", "ERROR", self.name)
                print(f"❌ Error en {self.name}: {e}")
                time.sleep(60)  # Esperar 1 minuto antes de reintentar
    
    @abstractmethod
    def work(self):
        """
        Método que debe implementar cada worker
        Este método se ejecuta en loop mientras el worker esté activo
        """
        pass
    
    def get_sleep_time(self) -> int:
        """
        Tiempo de espera entre ejecuciones (en segundos)
        Puede ser sobrescrito por cada worker
        """
        return 60  # Por defecto 1 minuto

