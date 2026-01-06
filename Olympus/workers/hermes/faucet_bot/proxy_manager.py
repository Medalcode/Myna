import os, json, time, requests

USAGE_FILE = os.path.join(os.path.dirname(__file__), "sessions", "proxy_usage.json")
MAX_USES = 50  # número máximo de usos antes de rotar

def load_usage():
    if os.path.exists(USAGE_FILE):
        try:
            with open(USAGE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_usage(data):
    os.makedirs(os.path.dirname(USAGE_FILE), exist_ok=True)
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def is_proxy_alive(proxy_str):
    """Comprueba rápidamente que el proxy responde y devuelve su IP pública.
    Utiliza httpbin.org/ip como endpoint ligero.
    """
    try:
        if "://" not in proxy_str:
            proxy_str = "http://" + proxy_str
        proxies = {"http": proxy_str, "https": proxy_str}
        resp = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=8)
        return resp.status_code == 200
    except Exception:
        return False

def get_next_proxy(proxies):
    """Devuelve el siguiente proxy válido y actualiza su contador de uso.
    Si todos los proxies están agotados o muertos, reinicia el contador.
    """
    usage = load_usage()
    # Orden aleatorio para distribuir carga
    for proxy in sorted(proxies, key=lambda _: os.urandom(1)):
        # Saltar si supera el máximo de usos
        if usage.get(proxy, 0) >= MAX_USES:
            continue
        if is_proxy_alive(proxy):
            usage[proxy] = usage.get(proxy, 0) + 1
            save_usage(usage)
            return proxy
    # Si llegamos aquí, reiniciamos contadores y elegimos uno aleatorio
    save_usage({})
    return random.choice(proxies) if proxies else None
