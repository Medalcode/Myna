import requests
import time
import base64

class CaptchaSolver:
    def __init__(self, api_key, provider="2captcha"):
        self.api_key = api_key
        self.provider = provider
        
    def solve_image_captcha(self, image_path):
        """
        Sube una imagen local a 2Captcha y espera el resultado.
        """
        if not self.api_key:
            print("[Captcha] ⚠️ No API Key configured. Skipping.")
            return None

        print(f"[Captcha] 🧩 Solving with {self.provider}...")
        
        try:
            with open(image_path, "rb") as f:
                img_str = base64.b64encode(f.read()).decode('utf-8')
            
            # 1. Enviar desafío
            payload = {
                "key": self.api_key,
                "method": "base64",
                "body": img_str,
                "json": 1
            }
            
            # TODO: Soportar otros proveedores en el futuro
            url_in = "http://2captcha.com/in.php"
            url_res = "http://2captcha.com/res.php"
            
            resp = requests.post(url_in, json=payload)
            if resp.status_code != 200:
                print(f"[Captcha] ❌ Error sending: {resp.text}")
                return None
                
            req_json = resp.json()
            if req_json.get("status") != 1:
                print(f"[Captcha] ❌ API Error: {req_json.get('request')}")
                return None
                
            request_id = req_json.get("request")
            print(f"[Captcha] ⏳ ID: {request_id}. Waiting...")
            
            # 2. Esperar resultado (Polling)
            for _ in range(20): # Máximo 100 segundos
                time.sleep(5)
                resp_res = requests.get(f"{url_res}?key={self.api_key}&action=get&id={request_id}&json=1")
                if resp_res.status_code == 200:
                    res_json = resp_res.json()
                    status = res_json.get("status")
                    result_text = res_json.get("request")
                    
                    if status == 1:
                        print(f"[Captcha] ✅ Solved: {result_text}")
                        return result_text
                    elif result_text == "CAPCHA_NOT_READY":
                        continue
                    else:
                        print(f"[Captcha] ❌ Error: {result_text}")
                        return None
            
            print("[Captcha] ⏰ Timeout waiting for solution.")
            return None

        except Exception as e:
            print(f"[Captcha] 💥 Exception: {e}")
            return None
