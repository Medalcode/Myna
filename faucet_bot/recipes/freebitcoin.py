from .base_recipe import BaseRecipe
import time
import random

class FreeBitcoinRecipe(BaseRecipe):
    name = "FreeBitco.in"
    start_url = "https://freebitco.in/?op=home"

    def run(self, page, logger):
        logger(f"   [Recipe] Iniciando FreeBitco.in...")
        
        # 1. Chequeo de Login
        if page.is_visible("#login_form_btc_address", timeout=5000):
            logger("   [Auth] Detectado formulario de login. (Se requiere login manual o cookies)")
            # Aquí idealmente cargaríamos cookies. Por ahora, si no está logueado, fallamos suavemente.
            # O podríamos intentar loguear si tuviéramos credenciales en el proxy config.
            return

        # 2. Cerrar popups molestos (común en freebitcoin)
        try:
            if page.is_visible(".pushpad_deny_button"):
                page.click(".pushpad_deny_button")
            page.evaluate("() => { if(window.close_box) window.close_box(); }")
        except:
            pass

        # 3. Buscar el botón de ROLL
        # A veces hay que scrollear
        logger("   [Nav] Buscando botón ROLL...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        
        if page.is_visible("#free_play_form_button"):
            # Verificar si hay captcha
            if page.is_visible("#h-captcha") or page.is_visible(".g-recaptcha"):
                logger("   [Captcha] ¡Captcha detectado! No podemos resolverlo aún.")
                # Aquí iría la llamada a 2Captcha
            else:
                logger("   [Action] ¡Click en ROLL!")
                page.click("#free_play_form_button")
                time.sleep(5)
                
                # Verificar resultado
                balance = page.inner_text("#balance")
                logger(f"   [Win] Nuevo balance: {balance}")
        else:
            # Quizás ya jugamos y hay cuenta regresiva
            if page.is_visible(".countdown_amount"):
                tiempo_restante = page.inner_text(".countdown_amount")
                logger(f"   [Wait] Aún falta tiempo: {tiempo_restante} minutos")
            else:
                logger("   [Info] No se encontró botón ni cuenta regresiva.")

        logger("   [Done] Receta finalizada.")
