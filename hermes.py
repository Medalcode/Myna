#!/usr/bin/env python3
"""
Hermes V4.0 - Autonomous Faucet Bot
Clean, standalone version without external dependencies
"""

import threading
import time
import os
import logging
import random
import sys
from datetime import datetime

# Add faucet_bot to path
sys.path.append(os.path.join(os.getcwd(), 'faucet_bot'))

# --- IMPORTS ---
try:
    from faucet_bot.main import FaucetBot, load_proxies
    from faucet_bot.database import oracle
    from faucet_bot.config_loader import load_config, save_config
    HERMES_AVAILABLE = True
except ImportError as e:
    HERMES_AVAILABLE = False
    print(f"❌ Error importing Hermes modules: {e}")
    print("Make sure you're in the Hermes directory and dependencies are installed.")
    sys.exit(1)

# Optional: Battery monitor (only works in Termux)
try:
    import subprocess
    import json
    TERMUX_AVAILABLE = True
except:
    TERMUX_AVAILABLE = False

# --- LOGGING SETUP ---
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'hermes.log'),
    level=logging.INFO,
    format='%(asctime)s | %(threadName)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- CONSOLE COLORS ---
VERDE = '\033[92m'
AZUL = '\033[94m'
AMARILLO = '\033[93m'
ROJO = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# --- GLOBAL STATE ---
status_hermes = "Iniciando..."
status_last_action = ""
running = True

# --- BATTERY MONITOR (TERMUX ONLY) ---
class BatteryMonitor:
    def __init__(self):
        self.last_status = {}
        self.available = TERMUX_AVAILABLE
    
    def get_status(self):
        """Get battery status from Termux API"""
        if not self.available:
            return None
        
        try:
            result = subprocess.run(
                ['termux-battery-status'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                self.last_status = data
                return data
        except:
            self.available = False
        
        return None
    
    def get_summary(self):
        """Get battery summary string"""
        status = self.get_status()
        if not status:
            return "N/A"
        
        icon = "🔋" if status.get("plugged") != "UNPLUGGED" else "🪫"
        return f"{icon} {status.get('percentage', 0)}% ({status.get('temperature', 0)}°C)"
    
    def check_health(self):
        """Check battery health status"""
        status = self.get_status()
        if not status:
            return "UNKNOWN"
        
        percentage = status.get("percentage", 100)
        status_text = status.get("status", "UNKNOWN")
        
        if percentage < 15 and status_text == "DISCHARGING":
            return "CRITICAL"
        elif percentage < 30 and status_text == "DISCHARGING":
            return "LOW"
        
        return "OK"

# --- CONFIGURATION WIZARD ---
def wizard_config():
    """Interactive configuration wizard for first-time setup"""
    config = load_config()
    
    # Check if already configured
    if config.get("cointiply", {}).get("email"):
        return  # Already configured
    
    print("\n" + "="*60)
    print(f"{AMARILLO}🚀 HERMES - CONFIGURACIÓN INICIAL{RESET}")
    print("="*60)
    print("\nBienvenido a Hermes! Vamos a configurar el bot.\n")
    
    # Cointiply credentials
    print(f"{AZUL}📧 CREDENCIALES DE COINTIPLY{RESET}")
    print("Ingresa tus credenciales de Cointiply.com:")
    email = input(f"{VERDE}Email > {RESET}").strip()
    password = input(f"{VERDE}Password > {RESET}").strip()
    
    if email and password:
        config["cointiply"]["email"] = email
        config["cointiply"]["password"] = password
    
    # Captcha API Key (optional)
    print(f"\n{AZUL}🧩 CAPTCHA SOLVER (OPCIONAL){RESET}")
    print("Para automatización completa, puedes usar 2Captcha.com")
    print("Costo: ~$0.50 USD por 1000 captchas")
    print("Presiona ENTER para saltar este paso.")
    
    api_key = input(f"{VERDE}API Key de 2Captcha > {RESET}").strip()
    if api_key:
        config["captcha"]["api_key"] = api_key
    
    # Save configuration
    save_config(config)
    
    print(f"\n{VERDE}✅ Configuración guardada exitosamente!{RESET}")
    print(f"\n{AMARILLO}⚠️ IMPORTANTE:{RESET}")
    print(f"  1. Añade tus proxies en: {BOLD}faucet_bot/proxies.txt{RESET}")
    print(f"  2. Formato: ip:puerto o user:pass@ip:puerto")
    print(f"  3. Un proxy por línea\n")
    
    input("Presiona ENTER cuando hayas configurado los proxies...")

# --- HERMES BOT THREAD ---
def bot_hermes_worker():
    """Main Hermes bot worker thread"""
    global status_hermes, status_last_action, running
    
    if not HERMES_AVAILABLE:
        status_hermes = f"{ROJO}Error: Módulos no disponibles{RESET}"
        return
    
    # Load proxies
    proxies_file = os.path.join(os.path.dirname(__file__), 'faucet_bot', 'proxies.txt')
    proxies = load_proxies(proxies_file)
    
    if not proxies:
        status_hermes = f"{AMARILLO}⚠️ No hay proxies configurados{RESET}"
        logging.warning("No proxies found. Bot cannot start.")
        return
    
    logging.info(f"Hermes started with {len(proxies)} proxies")
    
    # Load configuration
    config = load_config()
    cycle_delay = config.get("system", {}).get("cycle_delay_seconds", 3600)
    
    while running:
        cycle_start = time.time()
        
        for i, proxy in enumerate(proxies):
            if not running:
                break
            
            status_hermes = f"{AZUL}Cuenta {i+1}/{len(proxies)} | Proxy: {proxy[:25]}...{RESET}"
            logging.info(f"Starting session with proxy {proxy}")
            
            try:
                session_id = f"account_{i+1:03d}"
                bot = FaucetBot(proxy, session_id=session_id)
                
                status_last_action = f"Ejecutando recetas en {session_id}..."
                bot.run_recipes()
                
                status_hermes = f"{VERDE}✅ Sesión completada{RESET}"
                logging.info(f"Session {session_id} completed successfully")
                
            except Exception as e:
                status_hermes = f"{ROJO}❌ Error: {str(e)[:30]}...{RESET}"
                logging.error(f"Error in session with proxy {proxy}: {e}")
            
            # Human-like delay between accounts
            delay = random.randint(10, 30)
            for s in range(delay, 0, -1):
                if not running:
                    break
                time.sleep(1)
                status_last_action = f"Esperando próxima cuenta: {s}s"
        
        # Cycle completed, wait before next round
        elapsed = time.time() - cycle_start
        wait_for = max(60, cycle_delay - elapsed)
        
        status_hermes = f"{AMARILLO}Ciclo completado{RESET}"
        logging.info(f"Cycle completed. Waiting {wait_for}s before next round.")
        
        for m in range(int(wait_for), 0, -1):
            if not running:
                break
            if m % 10 == 0:
                status_last_action = f"Próximo ciclo en {m//60}min {m%60}s"
            time.sleep(1)

# --- DASHBOARD ---
def show_dashboard():
    """Display real-time dashboard in terminal"""
    global running
    
    print("\n🚀 Iniciando Hermes Dashboard...\n")
    time.sleep(1)
    
    # Initialize battery monitor
    battery = BatteryMonitor()
    
    # Run configuration wizard if needed
    wizard_config()
    
    try:
        while running:
            os.system('cls' if os.name == 'nt' else 'clear')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{BOLD}{'='*60}{RESET}")
            print(f"      🏛️  HERMES V4.0 - AUTONOMOUS FAUCET BOT")
            print(f"{'='*60}{RESET}")
            print(f"📅 {now}")
            
            # Battery info (if available)
            if battery.available:
                batt_info = battery.get_summary()
                batt_health = battery.check_health()
                color = ROJO if batt_health == "CRITICAL" else (AMARILLO if batt_health == "LOW" else VERDE)
                print(f"🔋 Batería: {color}{batt_info}{RESET}")
            
            print(f"📄 Logs: logs/hermes.log")
            print(f"{'-'*60}")
            
            # Hermes status
            print(f"\n🚀 [HERMES - Faucet Bot]:")
            
            # Load proxies count
            proxies_file = os.path.join(os.path.dirname(__file__), 'faucet_bot', 'proxies.txt')
            proxies = load_proxies(proxies_file)
            print(f"    └── Proxies: {len(proxies)}")
            print(f"    └── Estado: {status_hermes}")
            print(f"    └── Acción: {status_last_action}")
            
            # Statistics from database
            print(f"\n{'-'*60}")
            try:
                stats = oracle.get_stats()
                print(f"💰 {AMARILLO}BALANCE:{RESET}")
                print(f"    └── Total: {BOLD}{stats['total']} satoshis{RESET}")
                print(f"    └── Hoy: {stats['today']} sats")
                print(f"    └── Tasa de éxito: {stats['success_rate']}% ({stats['wins']}W / {stats['fails']}F)")
            except Exception as e:
                print(f"💰 Balance: {ROJO}Error cargando stats{RESET}")
            
            print(f"{'-'*60}")
            print(f"{AMARILLO}Presiona Ctrl+C para detener el bot{RESET}")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        running = False
        print(f"\n\n{AMARILLO}🛑 Deteniendo Hermes...{RESET}")

# --- MAIN ---
if __name__ == "__main__":
    print(f"""
{VERDE}
╦ ╦╔═╗╦═╗╔╦╗╔═╗╔═╗  ╦  ╦╦ ╦
╠═╣║╣ ╠╦╝║║║║╣ ╚═╗  ╚╗╔╝╚═╣
╩ ╩╚═╝╩╚═╩ ╩╚═╝╚═╝   ╚╝  ╩
{RESET}
Autonomous Faucet Bot - V4.0
Developed by MedalCode
    """)
    
    # Start bot worker thread
    t_hermes = threading.Thread(target=bot_hermes_worker, name="Hermes-Worker")
    t_hermes.daemon = True
    t_hermes.start()
    
    # Show dashboard (blocking)
    try:
        show_dashboard()
    except KeyboardInterrupt:
        running = False
    
    print(f"\n{VERDE}✅ Hermes detenido correctamente{RESET}\n")
