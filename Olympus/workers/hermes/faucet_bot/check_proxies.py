
import requests
import concurrent.futures
import time

def check_proxy(proxy_str):
    """
    Checks if a proxy is alive and measures its latency.
    Returns: (is_valid, latency_ms, real_ip)
    """
    proxy_config = {}
    if "://" not in proxy_str:
        proxy_str = "http://" + proxy_str
        
    try:
        # Construct proxy dict for requests
        # Note: requests proxy format is slightly different than Playwright
        # but usually accepts http://user:pass@host:port for 'http' key
        proxies = {
            "http": proxy_str,
            "https": proxy_str
        }
        
        start_time = time.time()
        # We query httpbin to see our IP
        resp = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=10)
        latency = (time.time() - start_time) * 1000
        
        if resp.status_code == 200:
            ip_info = resp.json()
            return True, latency, ip_info.get("origin", "Unknown")
        else:
            return False, 0, None
            
    except Exception:
        return False, 0, None

def main():
    print("--- 🕵️  HERMES PROXY CHECKER ---")
    try:
        with open("proxies.txt", "r") as f:
            proxies = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    except FileNotFoundError:
        print("Error: 'proxies.txt' not found.")
        return

    if not proxies:
        print("No proxies found in proxies.txt")
        return

    print(f"Testing {len(proxies)} proxies...")
    print("-" * 50)
    print(f"{'PROXY':<40} | {'STATUS':<10} | {'LATENCY':<10} | {'IP'}")
    print("-" * 50)

    good_proxies = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_proxy = {executor.submit(check_proxy, p): p for p in proxies}
        for future in concurrent.futures.as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                is_valid, latency, ip = future.result()
                status = "✅ OK" if is_valid else "❌ FAIL"
                lat_str = f"{latency:.0f}ms" if is_valid else "-"
                ip_str = ip if ip else "-"
                
                print(f"{proxy[:37]:<40} | {status:<10} | {lat_str:<10} | {ip_str}")
                
                if is_valid:
                    good_proxies.append(proxy)
                    
            except Exception as exc:
                print(f"{proxy:<40} | ❌ ERROR   | -          | -")

    print("-" * 50)
    print(f"Summary: {len(good_proxies)}/{len(proxies)} proxies satisfy connection requirements.")
    
    if len(good_proxies) > 0 and len(good_proxies) < len(proxies):
        print("\nTip: Remove failed proxies from 'proxies.txt' to improve bot stability.")

if __name__ == "__main__":
    main()
