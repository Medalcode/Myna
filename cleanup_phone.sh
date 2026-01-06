#!/data/data/com.termux/files/usr/bin/bash

# Script de Limpieza Total - Eliminar Proyectos Rotos
# Mantiene solo Hermes V4.0 limpio

set -e

echo "=================================================="
echo "  🧹 LIMPIEZA TOTAL DEL SISTEMA"
echo "=================================================="
echo ""
echo "⚠️  ADVERTENCIA: Este script eliminará:"
echo "   - Hestia (dashboard roto)"
echo "   - Hefesto (mobile farm con problemas de captcha)"
echo "   - Panoptes (scraper con datos ficticios)"
echo "   - Argos (trading bot abandonado)"
echo "   - Panteon SDK (complejidad innecesaria)"
echo ""
echo "✅ Se mantendrá:"
echo "   - Hermes V4.0 (único proyecto funcional)"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para confirmar
confirm() {
    read -p "¿Continuar con la limpieza? (escribe 'SI' para confirmar): " response
    if [ "$response" != "SI" ]; then
        echo -e "${YELLOW}Limpieza cancelada.${NC}"
        exit 0
    fi
}

# Pedir confirmación
confirm

echo ""
echo -e "${YELLOW}[1/6] Deteniendo procesos de proyectos rotos...${NC}"

# Matar procesos relacionados con proyectos abandonados
pkill -f "hestia" 2>/dev/null || true
pkill -f "hefesto" 2>/dev/null || true
pkill -f "panoptes" 2>/dev/null || true
pkill -f "argos" 2>/dev/null || true
pkill -f "cerbero" 2>/dev/null || true
pkill -f "panteon" 2>/dev/null || true

echo -e "${GREEN}✅ Procesos detenidos${NC}"

echo ""
echo -e "${YELLOW}[2/6] Eliminando directorios de proyectos rotos...${NC}"

# Ir al directorio padre de Hermes
cd "$(dirname "$(pwd)")" 2>/dev/null || cd ~

# Eliminar directorios (si existen)
if [ -d "Hestia" ]; then
    echo "   Eliminando Hestia..."
    rm -rf Hestia
    echo -e "${GREEN}   ✅ Hestia eliminado${NC}"
fi

if [ -d "Hefesto" ]; then
    echo "   Eliminando Hefesto..."
    rm -rf Hefesto
    echo -e "${GREEN}   ✅ Hefesto eliminado${NC}"
fi

if [ -d "Panoptes" ]; then
    echo "   Eliminando Panoptes..."
    rm -rf Panoptes
    echo -e "${GREEN}   ✅ Panoptes eliminado${NC}"
fi

if [ -d "Argos" ]; then
    echo "   Eliminando Argos..."
    rm -rf Argos
    echo -e "${GREEN}   ✅ Argos eliminado${NC}"
fi

echo ""
echo -e "${YELLOW}[3/6] Limpiando archivos obsoletos en Hermes...${NC}"

cd Hermes 2>/dev/null || { echo -e "${RED}Error: No se encontró directorio Hermes${NC}"; exit 1; }

# Eliminar archivos obsoletos de Hermes
rm -f olympus.py 2>/dev/null && echo "   ✅ olympus.py eliminado" || true
rm -f panteon.py 2>/dev/null && echo "   ✅ panteon.py eliminado" || true
rm -f hermes_db.py 2>/dev/null && echo "   ✅ hermes_db.py eliminado" || true
rm -f battery_monitor.py 2>/dev/null && echo "   ✅ battery_monitor.py eliminado" || true
rm -f make_update.py 2>/dev/null && echo "   ✅ make_update.py eliminado" || true
rm -f debug_import.py 2>/dev/null && echo "   ✅ debug_import.py eliminado" || true
rm -f olympus.db 2>/dev/null && echo "   ✅ olympus.db eliminado" || true
rm -f olympus_operations.log 2>/dev/null && echo "   ✅ olympus_operations.log eliminado" || true
rm -f update_hermes*.zip 2>/dev/null && echo "   ✅ Archivos ZIP antiguos eliminados" || true

echo -e "${GREEN}✅ Archivos obsoletos eliminados${NC}"

echo ""
echo -e "${YELLOW}[4/6] Limpiando bases de datos antiguas...${NC}"

# Eliminar bases de datos de proyectos rotos
rm -f hestia.db 2>/dev/null && echo "   ✅ hestia.db eliminado" || true
rm -f panteon.db 2>/dev/null && echo "   ✅ panteon.db eliminado" || true

echo -e "${GREEN}✅ Bases de datos antiguas eliminadas${NC}"

echo ""
echo -e "${YELLOW}[5/6] Verificando estructura de Hermes V4.0...${NC}"

# Verificar que existan los directorios necesarios
mkdir -p data
mkdir -p logs
mkdir -p faucet_bot/sessions

# Verificar archivos críticos
if [ -f "hermes.py" ]; then
    echo -e "${GREEN}   ✅ hermes.py presente${NC}"
else
    echo -e "${RED}   ❌ hermes.py NO ENCONTRADO${NC}"
fi

if [ -f "faucet_bot/database.py" ]; then
    echo -e "${GREEN}   ✅ faucet_bot/database.py presente${NC}"
else
    echo -e "${RED}   ❌ faucet_bot/database.py NO ENCONTRADO${NC}"
fi

if [ -f "faucet_bot/config.json" ]; then
    echo -e "${GREEN}   ✅ faucet_bot/config.json presente${NC}"
else
    echo -e "${YELLOW}   ⚠️  faucet_bot/config.json no encontrado (se creará en primer arranque)${NC}"
fi

if [ -d "data" ]; then
    echo -e "${GREEN}   ✅ Directorio data/ presente${NC}"
fi

if [ -d "logs" ]; then
    echo -e "${GREEN}   ✅ Directorio logs/ presente${NC}"
fi

echo ""
echo -e "${YELLOW}[6/6] Limpiando caché de Python...${NC}"

# Limpiar __pycache__ de proyectos rotos
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo -e "${GREEN}✅ Caché de Python limpiado${NC}"

echo ""
echo "=================================================="
echo -e "${GREEN}  ✅ LIMPIEZA COMPLETADA EXITOSAMENTE"
echo "=================================================="
echo ""
echo "📊 Resumen:"
echo "   ❌ Hestia - ELIMINADO"
echo "   ❌ Hefesto - ELIMINADO"
echo "   ❌ Panoptes - ELIMINADO"
echo "   ❌ Argos - ELIMINADO"
echo "   ❌ Archivos obsoletos - ELIMINADOS"
echo ""
echo "   ✅ Hermes V4.0 - LIMPIO Y LISTO"
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Configurar proxies:"
echo "   nano faucet_bot/proxies.txt"
echo ""
echo "2. Ejecutar Hermes:"
echo "   python hermes.py"
echo ""
echo "   O usar el script de inicio:"
echo "   ./start.sh"
echo ""
echo "=================================================="
