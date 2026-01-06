from .base_recipe import BaseRecipe
from config_loader import load_config
from captcha_solver import CaptchaSolver
import time
import random
import os

class CointiplyRecipe(BaseRecipe):
    name = "Cointiply"
    start_url = "https://cointiply.com/login"

    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.creds = self.config.get("cointiply", {})
        captcha_cfg = self.config.get("captcha", {})
        self.solver = CaptchaSolver(captcha_cfg.get("api_key"), captcha_cfg.get("provider"))

    def run(self, page, logger):
        logger(f"   [Recipe] Iniciando Cointiply (Version 3.0 - Config + Captcha)...")
        
        # 1. Login Inteligente
        # Si NO estamos logueados (verificando URL o selectores), intentamos login
        if "login" in page.url or page.is_visible("input[name='email']"):
             # ESPERAR HASTA 15 SEGUNDOS POR EL LOGIN
            try:
                if not self.creds.get("email") or not self.creds.get("password"):
                    logger("   [Auth] ❌ CREDENCIALES FALTANTES EN CONFIG.JSON!")
                    # Intentamos usar los valores hardcodeados de emergencia si falla la config
                    # (Backup temporal, aunque idealmente el usuario configura el json)
                    return

                page.wait_for_selector("input[name='email']", timeout=15000)
                logger("   [Auth] Formulario cargado. Entrando con credenciales de config...")
                
                page.fill("input[name='email']", self.creds.get("email")) 
                page.fill("input[name='password']", self.creds.get("password"))
                page.click("button:has-text('Log In')")
                
                # Esperar redirección o error
                time.sleep(10)
                
                if "home" in page.url or "roll-faucet" in page.url:
                    logger("   [Auth] ✅ Login exitoso.")
                else:
                    logger("   [Auth] ⚠️ Posible fallo de login (quizás captcha o 2FA).")

            except Exception as e:
                logger(f"   [Auth] Error intentando login: {e}")

        # 2. Navegar al Faucet
        logger("   [Nav] Yendo al Roll Faucet...")
        page.goto("https://cointiply.com/roll-faucet", timeout=60000)
        time.sleep(5)

        # 3. Detectar Botón y Captcha
        roll_btn = page.locator("button.btn-success:has-text('Roll & Win')")
        
        if roll_btn.count() > 0 and roll_btn.is_visible():
            logger("   [Action] Botón ROLL encontrado.")
            
            # --- LÓGICA CAPTCHA ---
            # Cointiply a veces muestra el captcha ANTES de clickear, a veces después.
            # Asumimos que hay que resolver antes si está visible.
            
            # Buscar desafío SolveMedia (imagen de texto)
            solvemedia_img = page.locator("#adcopy-puzzle-image-image") 
            solvemedia_input = page.locator("#adcopy_response")

            if solvemedia_img.count() > 0 and solvemedia_img.is_visible():
                logger("   [Captcha] Detectado SolveMedia. Intentando resolver...")
                
                # Screenshot del elemento
                img_path = f"captcha_{int(time.time())}.png"
                solvemedia_img.screenshot(path=img_path)
                
                # Resolver
                solution = self.solver.solve_image_captcha(img_path)
                if solution:
                    logger(f"   [Captcha] Solución: {solution}")
                    solvemedia_input.fill(solution)
                    try: os.remove(img_path) 
                    except: pass
                else:
                    logger("   [Captcha] ❌ No se pudo resolver (Falta API Key o Error).")
            
            # --- FIN LOGICA CAPTCHA ---

            logger("   [Action] Click ROLL...")
            roll_btn.click()
            time.sleep(5)
            
            # Verificar ganar
            if page.is_visible(".md-toast-content"):
                logger(f"   [Win] 🏆 {page.inner_text('.md-toast-content')}")
            else:
                logger("   [Check] Sin confirmación visual del premio.")
        else:
            logger("   [Info] Botón Roll no encontrado (¿Ya cobraste o timer activo?).")

        logger("   [Done] Receta finalizada.")
