import random
import time
import os
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

# Importar las recetas
try:
    from recipes import ACTIVE_RECIPES
    from database import oracle
except ImportError:
    try:
        from faucet_bot.recipes import ACTIVE_RECIPES
        from faucet_bot.database import oracle
    except:
        ACTIVE_RECIPES = []
        oracle = None
        print("[Error] No se pudieron importar las dependencias (recetas/db).")

class FaucetBot:
    def __init__(self, proxy_string, session_id="default"):
        self.proxy_config = self._parse_proxy(proxy_string)
        self.session_id = session_id
        self.sessions_dir = os.path.join(os.path.dirname(__file__), 'sessions')
        os.makedirs(self.sessions_dir, exist_ok=True)
        self.state_file = os.path.join(self.sessions_dir, f"{self.session_id}.json")
    
    def _parse_proxy(self, proxy_string):
        """Parses proxy string to dictionary."""
        try:
            if "://" not in proxy_string:
                proxy_string = "http://" + proxy_string
            parsed = urlparse(proxy_string)
            config = { "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}" }
            if parsed.username and parsed.password:
                config["username"] = parsed.username
                config["password"] = parsed.password
            return config
        except Exception as e:
            print(f"Error parsing proxy '{proxy_string}': {e}")
            return None

    def _human_like_behavior(self, page):
        """Simulates minimal human behavior."""
        print("   [Stealth] Simulating interaction...")
        try:
            page.evaluate("() => { try { window.scrollBy(0, window.innerHeight * Math.random()); } catch(e) {} }")
            time.sleep(random.uniform(1.0, 2.0))
        except Exception:
            pass

    def run_recipes(self, recipes=None):
        """
        Executes a list of recipes sequentially.
        """
        if recipes is None:
            recipes = ACTIVE_RECIPES

        if not self.proxy_config:
            print("   [Error] Invalid proxy. Skipping.")
            return

        with sync_playwright() as p:
            print(f"   [Init] Launching browser [Session: {self.session_id}]")
            
            try:
                # --- CONFIGURACIÓN DE SIGILO V2 ---
                # 1. User Agent Aleatorio
                try:
                    from fake_useragent import UserAgent
                    ua = UserAgent()
                    user_agent = ua.random
                    print(f"   [Stealth] Máscara: {user_agent[:25]}...")
                except:
                    user_agent = None

                # 2. Argumentos Anti-Detección Avanzados
                browser = p.chromium.launch(
                    headless=True, 
                    proxy=self.proxy_config,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-setuid-sandbox"
                    ]
                )
                
                context_options = {
                    "user_agent": user_agent,
                    "viewport": {'width': 1280, 'height': 720}
                }
                if os.path.exists(self.state_file):
                    print(f"   [Cookie] Loading session...")
                    context_options["storage_state"] = self.state_file
                
                context = browser.new_context(**context_options)
                page = context.new_page()
                
                stealth = Stealth()
                stealth.apply_stealth_sync(page)
                
                for recipe in recipes:
                    print(f"   \n--- Recipe: {recipe.name} ---")
                    max_retries = 3
                    for attempt in range(max_retries):
                        try:
                            print(f"   [Nav] {recipe.start_url} (Intento {attempt + 1}/{max_retries})")
                            page.goto(recipe.start_url, timeout=60000)
                            
                            self._human_like_behavior(page)
                            
                            recipe.run(page, logger=print)
                            
                            # Guardar estado
                            context.storage_state(path=self.state_file)
                            
                            # Registrar éxito en Oracle DB
                            if oracle:
                                amount_fake_demo = 10 if "Demo" in recipe.name else 0 
                                oracle.log_earning(
                                    self.session_id, 
                                    recipe.name, 
                                    amount_fake_demo, 
                                    self.proxy_config['server']
                                )

                            time.sleep(random.randint(3, 7))
                            break # Éxito, salir del bucle
                            
                        except Exception as e:
                            print(f"   [Warn] Error en {recipe.name}: {e}")
                            if attempt < max_retries - 1:
                                wait_time = 2 ** attempt
                                print(f"   [Retry] Reintentando en {wait_time}s...")
                                time.sleep(wait_time)
                            else:
                                print(f"   [Error] Receta {recipe.name} falló definitivamente.")
                                if oracle:
                                    oracle.log_earning(self.session_id, recipe.name, 0, self.proxy_config['server'], status=f"ERROR_FINAL: {e}")
                
                print("   [Done] All recipes finished.")
                browser.close()
                
            except Exception as e:
                print(f"   [Error] Browser session crashed: {e}")

def load_proxies(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

def main():
    proxies_file = 'proxies.txt'
    proxies = load_proxies(proxies_file)
    if not proxies: return
    print(f"Running standalone mode with {len(proxies)} proxies.")
    for i, proxy in enumerate(proxies):
        bot = FaucetBot(proxy, session_id=f"test_account_{i}")
        bot.run_recipes()
        break 

if __name__ == "__main__":
    main()
