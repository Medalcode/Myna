import os
import json
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

def load_proxies(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

def harvest_session(proxy_string, session_id, url="https://cointiply.com/login"):
    print(f"\n[{session_id}] Iniciando navegador para Login Manual...")
    
    # Parsear proxy manualmente porque FaucetBot está en main.py y queremos script aislado
    proxy_config = None
    if proxy_string:
        from urllib.parse import urlparse
        if "://" not in proxy_string:
            proxy_string = "http://" + proxy_string
        parsed = urlparse(proxy_string)
        proxy_config = { "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}" }
        if parsed.username:
            proxy_config["username"] = parsed.username
            proxy_config["password"] = parsed.password

    with sync_playwright() as p:
        # Lanzamos con HEADLESS=FALSE para que puedas ver y loguearte
        browser = p.chromium.launch(headless=False, proxy=proxy_config)
        
        # Check si ya existe sesion previa para cargarla
        sessions_dir = os.path.join(os.path.dirname(__file__), 'sessions')
        os.makedirs(sessions_dir, exist_ok=True)
        state_file = os.path.join(sessions_dir, f"{session_id}.json")
        
        context_opts = {}
        if os.path.exists(state_file):
            print(f"   [Info] Cargando cookies previas...")
            context_opts["storage_state"] = state_file
            
        context = browser.new_context(**context_opts)
        page = context.new_page()
        
        # Aplicamos stealth para que FreeBitcoin no sospeche al entrar
        stealth = Stealth()
        stealth.apply_stealth_sync(page)
        
        print(f"   [Nav] Yendo a {url}")
        try:
            page.goto(url, timeout=60000)
        except:
            print("   [Warn] Timeout cargando, pero el navegador sigue abierto.")

        print("\n" + "="*50)
        print(f" 🔐 ACCIÓN REQUERIDA PARA: {session_id}")
        print(" 1. En el navegador que se abrió, inicia sesión MANUALMENTE.")
        print(" 2. Resuelve cualquier Captcha.")
        print(" 3. Asegúrate de estar en el Dashboard principal.")
        print("="*50)
        
        input("   >>> Presiona ENTER aquí cuando hayas terminado de loguearte <<<")
        
        # Guardar las cookies de oro
        print(f"   [Save] Guardando sesión en {state_file}...")
        context.storage_state(path=state_file)
        
        print("   [Done] ¡Éxito! Cerrando navegador.")
        browser.close()

def main():
    proxies_file = os.path.join(os.path.dirname(__file__), 'proxies.txt')
    proxies = load_proxies(proxies_file)
    
    if not proxies:
        print("No se encontraron proxies en proxies.txt")
        return

    print("🌾 COSECHADOR DE COOKIES (Login Manual) 🌾")
    print("------------------------------------------")
    print(f"0. [SIN PROXY] Usar mi conexión real (Recomendado para generar cookies iniciales)")
    for i, proxy in enumerate(proxies):
        print(f"{i+1}. {proxy}")
    
    print("\nEscribe el número de la cuenta que quieres loguear (0 para sin proxy, o 'all'):")
    choice = input("> ")
    
    accounts_to_process = []
    
    if choice.lower() == 'all':
        accounts_to_process = list(enumerate(proxies))
    elif choice == '0':
        # Opción especial: Sin Proxy
        # Usamos el índice -1 como "cuenta sin proxy" o pedimos qué cuenta asignar
        print("¿A qué número de cuenta (1-28) quieres asignar esta sesión 'limpia'?")
        try:
            target_idx = int(input("> ")) - 1
            accounts_to_process = [(target_idx, None)] # None = Sin Proxy
        except:
            print("Número inválido.")
            return
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(proxies):
                accounts_to_process = [(idx, proxies[idx])]
            else:
                print("Índice inválido.")
        except ValueError:
            print("Entrada inválida.")
            
    for idx, proxy in accounts_to_process:
        session_name = f"account_{idx+1:03d}"
        harvest_session(proxy, session_name)
        
    print("\n✅ Cosecha terminada. Ahora copia la carpeta 'sessions' a tu celular.")

if __name__ == "__main__":
    main()
