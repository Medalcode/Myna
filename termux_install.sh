#!/bin/bash
# Installer for Hermes Faucet Bot on Android (Termux)

echo "📱 Iniciando Configuración de Hermes en Motorola..."

# 1. Actualizar Termux e instalar utilidades básicas
echo "[1/4] Actualizando paquetes de Termux..."
pkg update -y && pkg upgrade -y
pkg install proot-distro git wget -y

# 2. Instalar Ubuntu (El entorno virtual)
echo "[2/4] Instalando Ubuntu (esto puede tardar unos minutos)..."
proot-distro install ubuntu

# 3. Preparar el script de instalación interna (dentro de Ubuntu)
cat <<EOF > install_inside_ubuntu.sh
#!/bin/bash
echo "🐧 Configurando Ubuntu..."
apt update && apt upgrade -y

# Instalar Python y dependencias de sistema para Playwright
echo "📥 Instalando Python y dependencias..."
apt install -y python3 python3-pip python3-venv \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2

# Moverse al directorio del bot
cd /root/hermes

# Crear entorno virtual
echo "🐍 Creando Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

# Instalar liberías
echo "📦 Instalando librerías de Python..."
pip install -r faucet_bot/requirements.txt
pip install playwright
playwright install-deps
playwright install chromium

echo "✅ ¡Instalación Completa!"
echo "Para iniciar el bot ejecuta: ./start_bot.sh"
EOF
chmod +x install_inside_ubuntu.sh

# 4. Copiar archivos al entorno Ubuntu
echo "[3/4] Migrando Hermes a Ubuntu..."
# Asumimos que el usuario corre esto desde la carpeta donde copió los archivos
mkdir -p /data/data/com.termux/files/usr/var/lib/proot-distro/installed-rootfs/ubuntu/root/hermes
cp -r * /data/data/com.termux/files/usr/var/lib/proot-distro/installed-rootfs/ubuntu/root/hermes/
mv install_inside_ubuntu.sh /data/data/com.termux/files/usr/var/lib/proot-distro/installed-rootfs/ubuntu/root/

# 5. Crear script de arranque rápido
echo "[4/4] Creando acceso directo..."
echo "proot-distro login ubuntu -- bash -c 'cd /root/hermes && source venv/bin/activate && python olympus.py'" > start_hermes.sh
chmod +x start_hermes.sh

echo "🎉 ¡Todo Listo!"
echo "Para terminar la instalación (solo la primera vez), ejecuta:"
echo "proot-distro login ubuntu -- bash /root/install_inside_ubuntu.sh"
echo ""
echo "Luego, para usar el bot día a día, solo escribe:"
echo "./start_hermes.sh"
