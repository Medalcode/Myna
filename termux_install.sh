#!/data/data/com.termux/files/usr/bin/bash

# Hermes V4.0 - Termux Installation Script
# This script sets up Hermes bot on Android via Termux

set -e  # Exit on error

echo "=================================================="
echo "  🏛️  HERMES V4.0 - INSTALADOR PARA TERMUX"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Update packages
echo -e "${YELLOW}[1/6] Actualizando paquetes del sistema...${NC}"
pkg update -y && pkg upgrade -y

# Step 2: Install system dependencies
echo -e "${YELLOW}[2/6] Instalando dependencias del sistema...${NC}"
pkg install -y python python-pip git wget

# Step 3: Install Python dependencies
echo -e "${YELLOW}[3/6] Instalando dependencias de Python...${NC}"
pip install --upgrade pip
pip install -r faucet_bot/requirements.txt

# Step 4: Install Playwright
echo -e "${YELLOW}[4/6] Instalando Playwright...${NC}"
pip install playwright
playwright install chromium

# Step 5: Create necessary directories
echo -e "${YELLOW}[5/6] Creando estructura de directorios...${NC}"
mkdir -p data
mkdir -p logs
mkdir -p faucet_bot/sessions

# Step 6: Set permissions
echo -e "${YELLOW}[6/6] Configurando permisos...${NC}"
chmod +x hermes.py

# Optional: Install Termux:API for battery monitoring
echo ""
echo -e "${YELLOW}¿Deseas instalar Termux:API para monitoreo de batería? (s/n)${NC}"
read -r response
if [[ "$response" =~ ^([sS][iI]|[sS])$ ]]; then
    pkg install -y termux-api
    echo -e "${GREEN}✅ Termux:API instalado${NC}"
else
    echo -e "${YELLOW}⚠️ Termux:API no instalado. El monitoreo de batería no estará disponible.${NC}"
fi

echo ""
echo "=================================================="
echo -e "${GREEN}✅ INSTALACIÓN COMPLETADA${NC}"
echo "=================================================="
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Configura tus proxies:"
echo "   nano faucet_bot/proxies.txt"
echo ""
echo "2. Ejecuta Hermes:"
echo "   python hermes.py"
echo ""
echo "3. El asistente de configuración te guiará en el primer arranque"
echo ""
echo "📚 Para más información, consulta README.md"
echo ""
echo -e "${YELLOW}⚠️ IMPORTANTE:${NC}"
echo "   - Mantén el dispositivo conectado al cargador"
echo "   - Usa una app como 'Caffeine' para evitar que la CPU se duerma"
echo "   - Revisa los logs en: logs/hermes.log"
echo ""
