import os
import sys
import random
import time
from typing import List

# Añadir el directorio del bot al path
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_dir = os.path.join(current_dir, "faucet_bot")
sys.path.insert(0, bot_dir)

# Importar el bot original
from main import FaucetBot, load_proxies
from recipes import ACTIVE_RECIPES

# Importar clase base y DB de Olympus
from workers.base_worker import BaseWorker
from core.database import db

class HermesWorker(BaseWorker):
    """
    Worker que envuelve al FaucetBot original
    """
    def __init__(self):
        super().__init__("hermes")
        self.proxies = []
        self._load_config()
        
    def _load_config(self):
        """Carga configuración inicial"""
        proxy_file = os.path.join(bot_dir, "proxies.txt")
        if os.path.exists(proxy_file):
            self.proxies = load_proxies(proxy_file)
        else:
            db.log("No se encontró proxies.txt", "WARN", self.name)
            
    def get_sleep_time(self) -> int:
        """Tiempo aleatorio entre 30 y 60 minutos (para modo normal)"""
        # TODO: Leer configuración para saber si es Greedy o Normal
        return random.randint(1800, 3600)

    def work(self):
        """Ejecuta una ronda del bot"""
        if not self.proxies:
            db.log("No hay proxies disponibles", "ERROR", self.name)
            self._load_config() # Reintentar cargar
            time.sleep(60)
            return

        # Seleccionar proxy aleatorio
        proxy = random.choice(self.proxies)
        
        db.log(f"Iniciando ronda con proxy {proxy[:20]}...", "INFO", self.name)
        
        try:
            # Instanciar y ejecutar bot
            # Usamos un session_id basado en el proxy para mantener cookies
            session_id = f"session_{hash(proxy)}"
            bot = FaucetBot(proxy, session_id=session_id)
            
            # Ejecutar recetas
            # Nota: run_recipes devuelve stats o None? Revisar main.py
            # Por ahora asumimos que funciona y maneja sus errores
            bot.run_recipes(ACTIVE_RECIPES)
            
            db.log("Ronda finalizada correctamente", "INFO", self.name)
            
            # TODO: Extraer resultados reales del bot para guardarlos en OlympusDB
            # Por ahora solo logueamos que se corrió
            db.log_run(self.name, "WIN", proxy=proxy, details="Ronda completada")
            
        except Exception as e:
            db.log(f"Error crítico en ronda: {str(e)}", "ERROR", self.name)
            db.log_run(self.name, "ERROR", proxy=proxy, details=str(e))

