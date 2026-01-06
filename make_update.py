
import zipfile
import os

def zip_hermes():
    # Archivos a incluir en la actualización V3
    target_files = [
        'olympus.py',
        'panteon.py',
        'battery_monitor.py',
        'faucet_bot/__init__.py',
        'faucet_bot/main.py',
        'faucet_bot/config_loader.py',
        'faucet_bot/captcha_solver.py',
        'faucet_bot/requirements.txt',
        'faucet_bot/recipes/__init__.py',
        'faucet_bot/recipes/cointiply.py',
        'faucet_bot/recipes/base_recipe.py',
        'GUIA_MOTOROLA.md',
    ]
    
    # También incluimos la sesión si existe (para no perder el login si el usuario lo tiene)
    session_file = 'faucet_bot/sessions/account_001.json'
    if os.path.exists(session_file):
        target_files.append(session_file)

    output_filename = "update_hermes_v3.zip"
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in target_files:
            if os.path.exists(file):
                print(f"Adding {file}...")
                zipf.write(file)
            else:
                print(f"Warning: {file} not found.")
                
    print(f"\n✅ Created {output_filename}")
    print("Versión 3.0: Soporte Captcha, Configuración Externa y Monitor de Batería.")

if __name__ == "__main__":
    zip_hermes()
