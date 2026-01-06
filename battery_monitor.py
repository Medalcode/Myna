import subprocess
import json
import time

class BatteryMonitor:
    def __init__(self):
        self.last_status = {}

    def get_status(self):
        """
        Llama a termux-battery-status y devuelve un dict con info.
        Retorna None si falla (no instalado).
        """
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
            else:
                return None
        except FileNotFoundError:
            return None # Comando no existe
        except Exception as e:
            print(f"[Battery] Error: {e}")
            return None

    def check_health(self):
        """
        Devuelve advertencias si la batería está crítica.
        """
        status = self.get_status()
        if not status:
            return "UNKNOWN" # No hay sensor

        percentage = status.get("percentage", 100)
        plugged = status.get("plugged", "UNPLUGGED")
        status_text = status.get("status", "UNKNOWN") # CHARGING, DISCHARGING, FULL

        if percentage < 15 and status_text == "DISCHARGING":
            return "CRITICAL"
        elif percentage < 30 and status_text == "DISCHARGING":
            return "LOW"
        
        return "OK"

    def get_summary(self):
        if not self.last_status:
            return "Batería: --%"
        
        icon = "🔋" if self.last_status.get("plugged") != "UNPLUGGED" else "🪫"
        return f"{icon} {self.last_status.get('percentage')}% ({self.last_status.get('temperature', 0)}°C)"
