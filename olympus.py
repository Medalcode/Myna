import threading
import time
import os
import logging
import subprocess
import select
from datetime import datetime
import sys

# --- INTEGRACIÓN PANTEÓN (SDK) ---
try:
    from panteon import Panteon
    PANTEON_AVAILABLE = True
except ImportError:
    PANTEON_AVAILABLE = False
    print("⚠️ Panteon SDK no encontrado. Se usará modo local aislado.")

# --- HERMES BOT IMPORT ---
# Añadir el directorio actual al path para importar faucet_bot
sys.path.append(os.path.join(os.getcwd(),'faucet_bot'))
try:
    from faucet_bot.main import FaucetBot, load_proxies
    HERMES_AVAILABLE = True
except ImportError as e:
    # Fallback si no estamos en el directorio correcto
    try:
        sys.path.append(os.getcwd())
        from faucet_bot.main import FaucetBot, load_proxies
        HERMES_AVAILABLE = True
    except ImportError:
        HERMES_AVAILABLE = False
        print(f"Advertencia: No se pudo importar Hermes ({e})")

# --- MONITOR BATERÍA ---
try:
    from battery_monitor import BatteryMonitor
    BATTERY_AVAILABLE = True
except:
    BATTERY_AVAILABLE = False

# --- CONFIGURACIÓN DE LOGS (LEGACY + PANTEON) ---
logging.basicConfig(
    filename='olympus_operations.log',
    level=logging.INFO,
    format='%(asctime)s | %(threadName)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- COLORES DE CONSOLA ---
VERDE = '\033[92m'
AZUL = '\033[94m'
AMARILLO = '\033[93m'
ROJO = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

# --- RUTAS ---
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
PARENT_DIR = os.path.dirname(ROOT_DIR) 
ARGOS_DIR = os.path.join(PARENT_DIR, "Argos")

ARGOS_PYTHON = os.path.join(ARGOS_DIR, "venv/bin/python")
ARGOS_SCRIPT = os.path.join(ARGOS_DIR, "main.py")

# --- ESTADO GLOBAL ---
status_argos = "Esperando conexión..."
status_hermes = "Iniciando..."
status_last_action = ""
sats_cosechados = 0
running = True

# Inicializar Panteón para Hermes
if PANTEON_AVAILABLE:
    panteon_hermes = Panteon("HERMES")
else:
    panteon_hermes = None

def wizard_config():
    """Asistente de configuración inicial (evita usar Nano)"""
    try:
        from faucet_bot.config_loader import load_config, save_config
        config = load_config()
        
        # Chequeo de API Key de Captcha
        if not config.get("captcha", {}).get("api_key"):
            print("\n" + "="*50)
            print(f"{AMARILLO}🧩 CONFIGURACIÓN DE CAPTCHA SOLVER{RESET}")
            print("="*50)
            print("Para cobrar 24/7, Hermes necesita resolver captchas.")
            print("Ingresa tu API KEY de 2captcha.com (o presiona ENTER para saltar):")
            print(f"{AZUL}Tip: Cuesta ~$0.50 USD por 1000 captchas.{RESET}")
            
            key = input(f"\n{VERDE}API KEY > {RESET}").strip()
            
            if key:
                config["captcha"]["api_key"] = key
                
                # Preguntar también por credenciales de Cointiply si faltan
                if not config.get("cointiply", {}).get("email"):
                    print(f"\n{AMARILLO}📧 CREDENCIALES COINTIPLY{RESET}")
                    email = input("Email > ").strip()
                    password = input("Password > ").strip()
                    config["cointiply"]["email"] = email
                    config["cointiply"]["password"] = password
                
                save_config(config)
                print(f"\n{VERDE}✅ ¡Configuración Guardada! Arrancando...{RESET}")
                time.sleep(2)
            else:
                print(f"\n{ROJO}⚠️ Sin API Key. Hermes dependerá de la suerte.{RESET}")
                time.sleep(2)
    except Exception as e:
        print(f"Error en Wizard: {e}")

def log_event(source, message, level="INFO"):
    """Wrapper híbrido: Loguea en archivo local y envía a Panteón (Hestia)"""
    # 1. Log Local
    if level == "INFO": logging.info(f"[{source}] {message}")
    elif level == "WARNING": logging.warning(f"[{source}] {message}")
    elif level == "ERROR": logging.error(f"[{source}] {message}")
    
    # 2. Log Panteón (Remoto/Centralizado)
    if panteon_hermes and source == "HERMES":
        panteon_hermes.log(message, level)

def monitor_argos_subprocess():
    """Ejecuta Argos como subproceso y monitorea su salida"""
    global status_argos, running
    
    # Verificación de existencia de Argos
    if not os.path.exists(ARGOS_SCRIPT):
        status_argos = f"{ROJO}No se encontró Argos en {ARGOS_DIR}{RESET}"
        return

    log_event("ARGOS", "Iniciando subproceso de Argos...")
    
    try:
        process = subprocess.Popen(
            [ARGOS_PYTHON, "-u", ARGOS_SCRIPT],
            cwd=ARGOS_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        
        status_argos = f"{VERDE}Proceso iniciado (PID: {process.pid}){RESET}"
        
        while running and process.poll() is None:
            # Leer stdout línea por línea
            output = process.stdout.readline()
            if output:
                line = output.strip()
                if line and not line.startswith("DEBUG"): 
                    status_argos = f"{VERDE}{line[:70]}{RESET}"
            
            # Leer stderr
            err = process.stderr.readline()
            if err:
                log_event("ARGOS_ERR", err.strip(), "ERROR")
                # Si Argos falla, lo reportamos a Panteón
                if PANTEON_AVAILABLE:
                     panteon_hermes.log(f"Alerta Argos: {err.strip()}", "ERROR")

        if running:
            status_argos = f"{ROJO}Argos se detuvo inesperadamente{RESET}"
            if PANTEON_AVAILABLE: panteon_hermes.log("Argos se detuvo inesperadamente", "ERROR")
            
    except Exception as e:
        status_argos = f"{ROJO}Error ejecutando Argos: {e}{RESET}"
    finally:
        if process and process.poll() is None:
            process.terminate()

def bot_hermes_reales():
    """
    Ejecuta la lógica real de Hermes importada de faucet_bot.main
    """
    global status_hermes, status_last_action, sats_cosechados, running
    
    if not HERMES_AVAILABLE:
        status_hermes = f"{ROJO}Librería 'faucet_bot' no encontrada.{RESET}"
        return

    proxies_file = os.path.join(ROOT_DIR, 'faucet_bot', 'proxies.txt')
    proxies = load_proxies(proxies_file)

    if not proxies:
        status_hermes = f"{AMARILLO}¡Faltan Proxies! Configura proxies.txt{RESET}"
        log_event("HERMES", "No se encontraron proxies. Deteniendo hilo.", "WARNING")
        return

    log_event("HERMES", f"Iniciando rotación con {len(proxies)} proxies.")
    
    import random
    
    while running:
        cycle_start = time.time()
        
        # Obtener configuración dinámica de Hestia (Panteón)
        wait_cycle_seconds = 3600 # Default 1 hora
        if PANTEON_AVAILABLE:
            remote_delay = panteon_hermes.get_config("hermes_ciclo_delay")
            if remote_delay:
                try:
                    wait_cycle_seconds = int(remote_delay)
                    log_event("HERMES", f"Configuración sincronizada: Ciclo de {wait_cycle_seconds}s")
                except:
                    pass

        for i, proxy in enumerate(proxies):
            if not running: break
            
            status_hermes = f"{AZUL}Cuenta {i+1}/{len(proxies)} | Proxy: {proxy[:20]}...{RESET}"
            log_event("HERMES", f"Iniciando sesión con proxy {proxy}")
            
            try:
                # Instancia real de Hermes
                session_id = f"account_{i+1:03d}" 
                bot = FaucetBot(proxy, session_id=session_id)
                
                status_last_action = f"Ejecutando recetas en {session_id}..."
                
                # EJECUCIÓN REAL
                # Pasamos logger custom si fuera posible, pero Hermes usa print/logger interno.
                bot.run_recipes() 
                
                # Reporte de latido a Panteón
                if PANTEON_AVAILABLE:
                     panteon_hermes.log(f"Sesión completada: {session_id}", "INFO")

                status_hermes = f"{VERDE}Sesión finalizada correctamente.{RESET}"
                
            except Exception as e:
                status_hermes = f"{ROJO}Error en sesión: {e}{RESET}"
                log_event("HERMES", f"Error con proxy {proxy}: {e}", "ERROR")

            # Espera entre cuentas
            delay = random.randint(10, 30)
            for s in range(delay, 0, -1):
                if not running: break
                time.sleep(1)
                status_last_action = f"Esperando cambio de cuenta: {s}s"
        
        # Espera de ciclo
        elapsed = time.time() - cycle_start
        wait_for = max(60, wait_cycle_seconds - elapsed)
        
        status_hermes = f"{AMARILLO}Ciclo completado.{RESET}"
        log_event("HERMES", "Ciclo de cuentas completado. Durmiendo.")
        
        for m in range(int(wait_for), 0, -1):
            if not running: break
            if m % 10 == 0:
                status_last_action = f"Siguiente ciclo en {m//60} min {m%60} s"
            time.sleep(1)

def mostrar_pantalla():
    global running
    print("\nIniciando Dashboard...\n")
    time.sleep(1)
    
    # Inicializar Monitor Batería
    batt_monitor = BatteryMonitor() if BATTERY_AVAILABLE else None

    # Ejecutar Wizard si es necesario
    wizard_config()

    try:
        while running:
            os.system('cls' if os.name == 'nt' else 'clear')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{BOLD}=================================================={RESET}")
            panteon_status = f"{VERDE}ON ({panteon_hermes.modo}){RESET}" if PANTEON_AVAILABLE else f"{ROJO}OFF{RESET}"
            
            print(f"      🏛️  OLYMPUS COMMAND CENTER (PANTEON: {panteon_status})")
            print(f"=================================================={RESET}")
            print(f"📅 {now}")
            
            # --- INFO BATERÍA ---
            if batt_monitor:
                batt_monitor.get_status() # Refresh
                batt_info = batt_monitor.get_summary()
                batt_health = batt_monitor.check_health()
                color_batt = ROJO if batt_health == "CRITICAL" else (AMARILLO if batt_health == "LOW" else VERDE)
                print(f"🔋 Energía: {color_batt}{batt_info}{RESET}")
            else:
                 print(f"🔋 Energía: N/A (Instalar Termux:API)")

            print(f"📄 Logs: olympus_operations.log")
            print(f"--------------------------------------------------")
            print(f"")
            print(f"👁️  [ARGOS - Trading]:")
            print(f"    └── Estado: {status_argos}")
            print(f"")
            print(f"🚀 [HERMES - Faucets]:")
            proxies_loaded = load_proxies(os.path.join(ROOT_DIR, 'faucet_bot', 'proxies.txt')) if HERMES_AVAILABLE else []
            print(f"    └── Proxies Cargados: {len(proxies_loaded)}")
            print(f"    └── Estado: {status_hermes}")
            print(f"    └── Acción: {status_last_action}")
            print(f"")
            print(f"--------------------------------------------------")
            try:
                from faucet_bot.database import oracle
                stats = oracle.get_stats()
                balance_display = f"{stats['total']} Satoshis (Hoy: {stats['today']})"
            except:
                balance_display = f"N/A"
            
            print(f"💰 {AMARILLO}BALANCE ACUMULADO: {balance_display}{RESET}")
            print(f"--------------------------------------------------")
            print(f"Presiona Ctrl+C para detener todos los sistemas.")
            
            time.sleep(1)
    except KeyboardInterrupt:
        running = False

if __name__ == "__main__":
    t_hermes = threading.Thread(target=bot_hermes_reales, name="Hermes-Thread")
    t_argos = threading.Thread(target=monitor_argos_subprocess, name="Argos-Monitor")
    
    t_hermes.daemon = True
    t_argos.daemon = True
    
    t_hermes.start()
    t_argos.start()
    
    try:
        mostrar_pantalla()
    except KeyboardInterrupt:
        running = False
        print("\nApagando Olimpo...")
