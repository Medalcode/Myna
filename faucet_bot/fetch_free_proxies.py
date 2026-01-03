import requests
from bs4 import BeautifulSoup
import concurrent.futures

def get_free_proxies():
    print("⏳ Descargando lista de proxies gratuitos...")
    url = "https://free-proxy-list.net/"
    proxies = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table table-striped table-bordered')
        if table:
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                if columns:
                    ip = columns[0].text
                    port = columns[1].text
                    https = columns[6].text
                    # Preferimos proxies que soporten HTTPS
                    if https == 'yes':
                        proxies.append(f"http://{ip}:{port}")
    except Exception as e:
        print(f"❌ Error descargando proxies: {e}")
    
    return proxies

def check_proxy(proxy):
    try:
        # Intentamos conectar a Google o httpbin con timeout corto
        resp = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=3)
        if resp.status_code == 200:
            return proxy
    except:
        return None

def main():
    raw_proxies = get_free_proxies()
    print(f"📋 Se encontraron {len(raw_proxies)} candidatos. Verificando cuáles funcionan (esto tomará unos segundos)...")
    
    working_proxies = []
    
    # Usamos hilos para verificar rápido
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(check_proxy, raw_proxies[:50]) # Probamos solo los primeros 50 para no tardar mucho
        
    for p in results:
        if p:
            working_proxies.append(p)

    print(f"\n✅ Se encontraron {len(working_proxies)} proxies funcionales.")
    
    if working_proxies:
        with open("proxies.txt", "w") as f:
            for p in working_proxies:
                f.write(p + "\n")
        print("💾 Guardados en 'proxies.txt'. ¡Listo para usar Hermes!")
    else:
        print("⚠️ No se encontraron proxies funcionales en este momento. Intenta más tarde o usa proxies de pago.")

if __name__ == "__main__":
    main()
