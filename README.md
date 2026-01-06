# Hermes V3.1: Mobile Autonomous Faucet Bot ⚡📱

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

Hermes es un bot autónomo diseñado para operar 24/7 en dispositivos Android (vía Termux) o servidores Linux. Su objetivo principal es interactuar con faucets de criptomonedas (actualmente **Cointiply**) de manera indetectable, gestionando sesiones, proxies y resolución de captchas.

## ✨ Características Principales

- **⚡ 100% Autónomo**: Diseñado para "Fire & Forget". Se ejecuta en segundo plano en tu teléfono.
- **📱 Nativo para Termux**: Optimizado para correr en entornos móviles con batería limitada.
- **🕵️ Evasión Avanzada**: Utiliza `playwright-stealth` y patrones de comportamiento humano aleatorios.
- **🔄 Rotación de Proxies Inteligente**: Chequeo de salud automático y rotación de IPs para evitar baneos.
- **💾 Base de Datos Local**: Registro detallado de cada ejecución (ganancias, errores) en SQLite (`hermes.db`).
- **📊 Dashboard en Terminal**: Interfaz visual para monitorear estado, batería y últimas ganancias.
- **🧩 Captcha Solver (Opcional)**: Integración lista para usar con **2Captcha** (requiere API Key).

## 🚀 Instalación Rápida (Android / Termux)

1.  **Instalar Termux y dependencias:**

    ```bash
    pkg update && pkg upgrade -y
    pkg install proot-distro git python -y
    proot-distro install ubuntu
    proot-distro login ubuntu
    ```

2.  **Clonar y configurar:**

    ```bash
    git clone https://github.com/MedalCode/Hermes.git
    cd Hermes
    bash termux_install.sh  # Instala Playwright, dependencias y venv
    ```

3.  **Ejecutar:**
    ```bash
    source venv/bin/activate
    python3 olympus.py
    ```

## ⚙️ Configuración

Al primer inicio, el **Asistente de Configuración** te guiará:

1.  **Proxies**: Añade tus proxies en `faucet_bot/proxies.txt` (formato `ip:puerto` o `user:pass@ip:puerto`).
2.  **Credenciales**: Ingresa tu usuario/pass de Cointiply cuando se solicite.
3.  **Captcha**: (Opcional) Ingresa tu API Key de 2Captcha para automatización total.

## 📂 Estructura del Proyecto

- `olympus.py`: **Cerebro**. Orquestador principal, dashboard y monitor de procesos.
- `faucet_bot/`: Núcleo del bot de navegación.
  - `main.py`: Lógica de rotación y ejecución de recetas.
  - `recipes/`: Scripts específicos para cada sitio (e.g., `cointiply.py`).
  - `proxy_manager.py`: Sistema de salud y selección de proxies.
- `hermes_db.py`: Módulo de base de datos SQLite y reportes.
- `BITACORA_HERMES.md`: Historial de cambios y roadmap.

## 🤝 Contribuciones & Roadmap

Revisa `BITACORA_HERMES.md` para ver el estado actual y tareas pendientes.
¡PRs bienvenidas! Especialmente para nuevas recetas de faucets o mejoras en la evasión.

---

**Disclaimer**: Este software es para fines educativos. El uso de bots puede violar los Términos de Servicio de algunos sitios web. Úsalo bajo tu propia responsabilidad.
