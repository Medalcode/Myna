from .base_recipe import BaseRecipe
import time
import random

class SannySoftRecipe(BaseRecipe):
    name = "SannySoft Test"
    start_url = "https://bot.sannysoft.com/"

    def run(self, page, logger):
        logger(f"   [Recipe] Ejecutando: {self.name}")
        
        # Esperar a que cargue la tabla de resultados
        page.wait_for_selector("table", timeout=15000)
        
        # Leer algún dato para verificar que estamos dentro
        webdriver_status = page.eval_on_selector("#webdriver-result", "el => el.textContent")
        logger(f"   [Check] WebDriver detectado: {webdriver_status}")
        
        # Simular lectura humana
        logger("   [Action] Scrolleando para leer resultados...")
        page.keyboard.press("PageDown")
        time.sleep(random.uniform(2, 4))
        page.keyboard.press("PageUp")
        
        logger("   [Done] Test finalizado.")
