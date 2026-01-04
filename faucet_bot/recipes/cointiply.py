from .base_recipe import BaseRecipe
import time
import random

class CointiplyRecipe(BaseRecipe):
    name = "Cointiply"
    start_url = "https://cointiply.com/home"

    def run(self, page, logger):
        logger(f"   [Recipe] Iniciando Cointiply...")
        
        # 1. Chequeo de Login
        # Si vemos el botón de "Login" o "Register", es que estamos fuera
        if page.is_visible("a[href='/login']") or page.is_visible("button:has-text('Log In')"):
            logger("   [Auth] No detecto sesión activa. Se requieren cookies.")
            return

        # 2. Navegar al Faucet
        # A veces sale un popup de bienvenida
        try:
            if page.is_visible("button.btn-primary:has-text('Maybe Later')"):
                page.click("button.btn-primary:has-text('Maybe Later')")
        except:
            pass

        logger("   [Nav] Yendo al Roll Faucet...")
        page.goto("https://cointiply.com/roll-faucet", timeout=60000)
        time.sleep(random.uniform(3, 5))

        # 3. Buscar botón "Roll & Win"
        roll_btn_selector = "button.btn-success:has-text('Roll & Win')"
        
        if page.is_visible(roll_btn_selector):
            logger("   [Action] Botón ROLL encontrado.")
            
            # Cointiply SIEMPRE pide captcha.
            # Por ahora, intentaremos hacer clic en el botón. 
            # Si el captcha es simple (texto), a veces pasa. Si no, fallará hasta que integremos 2Captcha.
            
            logger("   [Sim] Intentando ROLL (puede requerir captcha humano)...")
            page.click(roll_btn_selector)
            time.sleep(5)
            
            # Verificar si ganamos
            if page.is_visible(".md-toast-content"):
                msg = page.inner_text(".md-toast-content")
                logger(f"   [Win] Resultado: {msg}")
            else:
                logger("   [Check] No vi confirmación. ¿Captcha pendiente?")
        else:
            # Quizás ya cobramos
            if page.is_visible(".time-remaining"):
                wait_time = page.inner_text(".time-remaining")
                logger(f"   [Wait] Faucet en enfriamiento: {wait_time}")
            else:
                logger("   [Info] No encontré botón ni timer.")

        logger("   [Done] Receta Cointiply terminada.")
