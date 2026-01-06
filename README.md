# Hermes V4.0: Autonomous Faucet Bot ⚡

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

**Hermes** es un bot autónomo diseñado para operar 24/7 en dispositivos Android (vía Termux) o servidores Linux. Interactúa con faucets de criptomonedas (actualmente **Cointiply**) de manera indetectable, gestionando sesiones, proxies y resolución de captchas.

## ✨ Características Principales

- **⚡ 100% Autónomo**: Diseñado para "Fire & Forget". Se ejecuta en segundo plano.
- **📱 Nativo para Termux**: Optimizado para entornos móviles con batería limitada.
- **🕵️ Evasión Avanzada**: Utiliza `playwright-stealth` y patrones de comportamiento humano.
- **🔄 Rotación de Proxies**: Chequeo de salud automático y rotación inteligente de IPs.
- **💾 Base de Datos Local**: Registro detallado en SQLite (`data/hermes.db`).
- **📊 Dashboard en Terminal**: Interfaz visual para monitorear estado y ganancias.
- **🧩 Captcha Solver**: Integración con **2Captcha** (opcional).
- **🧹 Sin Dependencias Externas**: Versión limpia y autocontenida.

## 🚀 Instalación Rápida

### En PC (Linux/Mac)

```bash
# 1. Clonar repositorio
git clone https://github.com/MedalCode/Hermes.git
cd Hermes

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r faucet_bot/requirements.txt
playwright install chromium

# 4. Ejecutar
python3 hermes.py
```

### En Android (Termux)

```bash
# 1. Instalar Termux desde F-Droid (NO desde Play Store)
# 2. Actualizar paquetes
pkg update && pkg upgrade -y

# 3. Instalar dependencias del sistema
pkg install python git -y

# 4. Clonar y configurar
git clone https://github.com/MedalCode/Hermes.git
cd Hermes
bash termux_install.sh

# 5. Ejecutar
python hermes.py
```

## ⚙️ Configuración

Al primer inicio, el **Asistente de Configuración** te guiará:

### 1. Credenciales de Cointiply

- Email y contraseña de tu cuenta

### 2. Proxies (OBLIGATORIO)

Edita `faucet_bot/proxies.txt` y añade tus proxies:

```
# Formato simple
123.45.67.89:8080
98.76.54.32:3128

# Con autenticación
user:pass@123.45.67.89:8080
```

### 3. Captcha Solver (Opcional)

- API Key de [2Captcha.com](https://2captcha.com)
- Costo aproximado: $0.50 USD por 1000 captchas

## 📂 Estructura del Proyecto

```
Hermes/
├── hermes.py              # 🎯 Punto de entrada principal
├── faucet_bot/
│   ├── main.py            # Core del bot
│   ├── database.py        # Gestión de SQLite
│   ├── config.json        # Configuración
│   ├── config_loader.py   # Cargador de config
│   ├── captcha_solver.py  # Solver de captchas
│   ├── proxy_manager.py   # Gestión de proxies
│   ├── proxies.txt        # Lista de proxies
│   ├── requirements.txt   # Dependencias Python
│   └── recipes/           # Recetas por sitio
│       ├── base_recipe.py
│       └── cointiply.py   # Receta de Cointiply
├── data/
│   └── hermes.db          # Base de datos SQLite
├── logs/
│   └── hermes.log         # Logs del bot
└── README.md
```

## 🎮 Uso

### Ejecución Normal

```bash
python3 hermes.py
```

### Ejecución en Segundo Plano (Linux/Termux)

```bash
nohup python3 hermes.py > /dev/null 2>&1 &
```

### Ver Logs en Tiempo Real

```bash
tail -f logs/hermes.log
```

### Detener el Bot

- En modo interactivo: `Ctrl+C`
- En segundo plano: `pkill -f hermes.py`

## 📊 Dashboard

El dashboard muestra en tiempo real:

- 🔋 **Estado de batería** (solo en Termux)
- 🌐 **Proxies cargados**
- 📈 **Estado actual** del bot
- 💰 **Balance total** y del día
- 📊 **Tasa de éxito** (WIN/FAIL ratio)

## 🗄️ Base de Datos

Hermes almacena toda la información en `data/hermes.db`:

### Tablas:

- **runs**: Registro detallado de cada ejecución
- **earnings**: Resumen de ganancias
- **proxy_health**: Estado de salud de proxies

### Consultar Estadísticas:

```bash
sqlite3 data/hermes.db "SELECT * FROM runs ORDER BY timestamp DESC LIMIT 10;"
```

## 🔧 Configuración Avanzada

Edita `faucet_bot/config.json`:

```json
{
  "system": {
    "headless": true, // Navegador sin interfaz
    "cycle_delay_seconds": 3600, // Espera entre ciclos (1h)
    "retry_attempts": 3, // Reintentos por receta
    "human_delay_min": 10, // Delay mínimo entre cuentas
    "human_delay_max": 30 // Delay máximo entre cuentas
  }
}
```

## 🛡️ Seguridad

- ✅ Nunca compartas tu `config.json` (contiene credenciales)
- ✅ Usa proxies de calidad para evitar baneos
- ✅ No ejecutes múltiples instancias con la misma cuenta
- ✅ Revisa los logs periódicamente

## 🐛 Troubleshooting

### Error: "No module named 'playwright'"

```bash
pip install playwright
playwright install chromium
```

### Error: "No proxies loaded"

Asegúrate de tener proxies en `faucet_bot/proxies.txt` (uno por línea).

### El bot se detiene con errores de captcha

Configura tu API Key de 2Captcha en `config.json`.

### Batería se agota rápido (Termux)

- Reduce `cycle_delay_seconds` a valores más altos (ej: 7200 = 2 horas)
- Mantén el dispositivo conectado al cargador
- Usa una app como "Caffeine" para evitar que la CPU se duerma

## 📝 Changelog

### V4.0 (2026-01-06)

- 🧹 **Reformulación completa**: Eliminadas dependencias de Panteon, Hestia, Argos
- 🗄️ **Base de datos unificada**: Nuevo módulo `database.py`
- 📊 **Dashboard mejorado**: Estadísticas en tiempo real
- ⚙️ **Configuración simplificada**: Wizard interactivo
- 📁 **Estructura limpia**: Directorios `data/` y `logs/`

### V3.1 (2026-01-05)

- ✅ Sistema de logging en SQLite
- ✅ Rotación inteligente de proxies
- ✅ Integración con 2Captcha

## 🤝 Contribuciones

¡PRs bienvenidas! Especialmente para:

- 🆕 Nuevas recetas de faucets
- 🛡️ Mejoras en evasión de detección
- 📊 Mejoras en el dashboard
- 🐛 Corrección de bugs

## 📄 Licencia

MIT License - Ver `LICENSE` para más detalles.

## ⚠️ Disclaimer

Este software es para **fines educativos**. El uso de bots puede violar los Términos de Servicio de algunos sitios web. Úsalo bajo tu propia responsabilidad.

---

**Desarrollado por [MedalCode](https://github.com/MedalCode)** 🏅
