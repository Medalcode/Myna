import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

DEFAULT_CONFIG = {
    "cointiply": {
        "email": "",
        "password": "",
        "active": True
    },
    "captcha": {
        "provider": "2captcha",
        "api_key": "" 
    },
    "system": {
        "headless": True,
        "proxy_file": "proxies.txt"
    }
}

def load_config():
    """
    Carga la configuración desde config.json.
    Si no existe, devuelve la configuración por defecto (y crea el archivo de ejemplo).
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                # Merge con default para asegurar que existan todas las claves
                # (Simple merge, level 1)
                for key, val in DEFAULT_CONFIG.items():
                    if key not in user_config:
                        user_config[key] = val
                    elif isinstance(val, dict):
                        for subkey, subval in val.items():
                            if subkey not in user_config[key]:
                                user_config[key][subkey] = subval
                return user_config
        except Exception as e:
            print(f"[Config] ⚠️ Error loading config.json: {e}")
            return DEFAULT_CONFIG
    else:
        # Crear archivo plantilla si no existe
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config_data):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
        print(f"[Config] ✅ Saved new configuration to {CONFIG_FILE}")
    except Exception as e:
        print(f"[Config] ❌ Error saving config: {e}")
