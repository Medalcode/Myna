#!/data/data/com.termux/files/usr/bin/bash
echo "📦 Instalando Olympus V4.0..."

# Ir al home
cd ~

# Verificar si existe el archivo
if [ ! -f /sdcard/olympus_deploy.tar.gz ]; then
    echo "❌ No se encontró olympus_deploy.tar.gz en /sdcard/"
    exit 1
fi

# Copiar y extraer
cp /sdcard/olympus_deploy.tar.gz .
echo "📂 Descomprimiendo..."
tar -xzf olympus_deploy.tar.gz
rm olympus_deploy.tar.gz

# Entrar a Olympus
cd Olympus

echo "🏗️ Instalando dependencias..."
# Instalar dependencias globales y del worker Hermes
pip install -r workers/hermes/faucet_bot/requirements.txt
playwright install chromium

echo "✅ Olympus instalado correctamente."
echo "🚀 Para iniciar, ejecuta: python3 olympus.py"
