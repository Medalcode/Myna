import threading
import time
import os
import logging
import subprocess
import select
from datetime import datetime
import sys

# --- MODIFICACIÓN IMPORTANTE ---
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

# --- CONFIGURACIÓN DE LOGS ---
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

# --- RUTAS DE ARGOS (Configuración) ---
# --- RUTAS DE ARGOS (Configuración Dinámica) ---
# Busca la carpeta Argos "al lado" de la carpeta Hermes
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # .../Hermes
PARENT_DIR = os.path.dirname(ROOT_DIR) # .../Antigravity (o Downloads en el cel)
ARGOS_DIR = os.path.join(PARENT_DIR, "Argos")

ARGOS_PYTHON = os.path.join(ARGOS_DIR, "venv/bin/python")
ARGOS_SCRIPT = os.path.join(ARGOS_DIR, "main.py")

# --- ESTADO GLOBAL ---
status_argos = "Esperando conexión..."
status_hermes = "Iniciando..."
status_last_action = ""
sats_cosechados = 0
running = True

def log_event(source, message, level="INFO"):
    if level == "INFO": logging.info(f"[{source}] {message}")
    elif level == "WARNING": logging.warning(f"[{source}] {message}")
    elif level == "ERROR": logging.error(f"[{source}] {message}")

def monitor_argos_subprocess():
    """Ejecuta Argos como subproceso y monitorea su salida"""
    global status_argos, running
    
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
            output = process.stdout.readline()
            if output:
                line = output.strip()
                if line and not line.startswith("DEBUG"): # Filtrar ruido si es necesario
                    status_argos = f"{VERDE}{line[:70]}{RESET}"
            
            err = process.stderr.readline()
            if err:
                log_event("ARGOS_ERR", err.strip(), "ERROR")
                
        if running:
            status_argos = f"{ROJO}Argos se detuvo inesperadamente{RESET}"
            
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

    proxies_file = os.path.join(os.getcwd(), 'faucet_bot', 'proxies.txt')
    proxies = load_proxies(proxies_file)
    target_url = "https://bot.sannysoft.com/" # URL DE PRUEBA INICIAL

    if not proxies:
        status_hermes = f"{AMARILLO}¡Faltan Proxies! Configura proxies.txt{RESET}"
        log_event("HERMES", "No se encontraron proxies. Deteniendo hilo.", "WARNING")
        return

    log_event("HERMES", f"Iniciando rotación con {len(proxies)} proxies.")
    
    import random
    
    while running:
        cycle_start = time.time()
        
        for i, proxy in enumerate(proxies):
            if not running: break
            
            status_hermes = f"{AZUL}Cuenta {i+1}/{len(proxies)} | Proxy: {proxy[:20]}...{RESET}"
            log_event("HERMES", f"Iniciando sesión con proxy {proxy}")
            
            try:
                # Instancia real de Hermes con Persistencia
                session_id = f"account_{i+1:03d}" # e.g. account_001
                bot = FaucetBot(proxy, session_id=session_id)
                
                status_last_action = f"Ejecutando recetas en {session_id}..."
                # Ya no pasamos target_url, Hermes usa las recetas activas internamente
                bot.run_recipes() 
                
                # Simulación de ganancia para demo (ya que bot.sannysoft no da dinero)
                if "sannysoft" in target_url:
                    sats_cosechados += 0 # No sumar fake en prod, o descomentar para test
                    status_last_action = "Test de detección completado (ver navegador)"
                else:
                    sats_cosechados += 10 # Placeholder
                    
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
        
        # Espera de ciclo (1 hora aprox)
        elapsed = time.time() - cycle_start
        wait_cycle = max(60, 3600 - elapsed)
        
        status_hermes = f"{AMARILLO}Ciclo completado.{RESET}"
        log_event("HERMES", "Ciclo de cuentas completado. Durmiendo hasta la próxima hora.")
        
        # Espera larga dividida en chunks para poder interrumpir
        for m in range(int(wait_cycle), 0, -1):
            if not running: break
            if m % 10 == 0:
                status_last_action = f"Siguiente ciclo en {m//60} min {m%60} s"
            time.sleep(1)

def mostrar_pantalla():
    global running
    print("\nIniciando Dashboard...\n")
    time.sleep(1)
    
    try:
        while running:
            os.system('cls' if os.name == 'nt' else 'clear')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"{BOLD}=================================================={RESET}")
            print(f"      🏛️  OLYMPUS COMMAND CENTER (PRODUCCIÓN){RESET}")
            print(f"=================================================={RESET}")
            print(f"📅 {now}")
            print(f"📄 Logs: olympus_operations.log")
            print(f"--------------------------------------------------")
            print(f"")
            print(f"👁️  [ARGOS - Trading]:")
            print(f"    └── Estado: {status_argos}")
            print(f"")
            print(f"🚀 [HERMES - Faucets]:")
            proxies_loaded = load_proxies(os.path.join(os.getcwd(), 'faucet_bot', 'proxies.txt')) if HERMES_AVAILABLE else []
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
                balance_display = f"{sats_cosechados} Satoshis (Memoria)"
            
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
