
import zipfile
import os

def zip_hermes():
    # Archivos a incluir en la actualización
    target_files = [
        'olympus.py',
        'faucet_bot/__init__.py',
        'faucet_bot/main.py',
        'faucet_bot/requirements.txt',
        'faucet_bot/recipes/__init__.py',
        'faucet_bot/recipes/cointiply.py',
        'faucet_bot/recipes/base_recipe.py',
        'GUIA_MOTOROLA.md',
    ]
    
    # También incluimos la sesión si existe
    session_file = 'faucet_bot/sessions/account_001.json'
    if os.path.exists(session_file):
        target_files.append(session_file)

    output_filename = "update_hermes.zip"
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in target_files:
            if os.path.exists(file):
                print(f"Adding {file}...")
                zipf.write(file)
            else:
                print(f"Warning: {file} not found.")
                
    print(f"\n✅ Created {output_filename}")
    print("Mueve este archivo a tu celular y ejecútalo.")

if __name__ == "__main__":
    zip_hermes()
