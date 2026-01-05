# 🦅 Proyecto Hermes: Automatización Distribuida (Mobile Cloud)

Hermes es una red de bots autónomos diseñados para operar en dispositivos móviles de bajo consumo (Android/Termux), orquestados centralmente por Hestia y supervisados vía Panteón SDK.

## 🚀 Características Principales

1.  **Arquitectura Móvil-Nativa**: Diseñado para correr 24/7 en teléfonos reciclados usando Termux + Ubuntu (Proot).
2.  **Mente de Enjambre (Hestia + Panteón)**:
    - **Panteon SDK**: Librería de integración que conecta Hermes con el cerebro central Hestia.
    - Configuración remota de ciclos y pausas.
    - Logging centralizado de errores y ganancias.
3.  **Stealth Avanzado**:
    - Rotación de Proxies por sesión.
    - Inyección de User-Agents realistas (fake-useragent).
    - Persistencia de Cookies para evasión de Captchas.
4.  **Objetivos Activos**:
    - 🟢 **Cointiply**: Automatización de Roll Faucet con espera inteligente de Login.
    - 🔴 **FreeBitcoin**: (Desactivado/Legacy).

## 📂 Nueva Estructura del Proyecto

- **`olympus.py`**: Centro de Mando Local. Muestra estado en tiempo real, saldos y logs.
- **`panteon.py`**: SDK de comunicación. Si detecta Hestia (Local o Remoto), envía telemetría.
- **`faucet_bot/`**:
  - `main.py`: Motor V8 de navegación (Playwright).
  - `recipes/`: Lógica específica por sitio (e.g. `cointiply.py`).
  - `sessions/`: Almacenamiento de cookies persistentes.
- **`GUIA_MOTOROLA.md`**: Guía paso a paso para despliegue en hardware específico.

## 📱 Instalación en Android (Termux)

1.  **Entorno Base**:

    ```bash
    pkg install proot-distro
    proot-distro install ubuntu
    proot-distro login ubuntu
    ```

2.  **Despliegue Rápido (vía Zip)**:
    Transfiere `update_hermes_v2.zip` al dispositivo:

    ```bash
    cp /sdcard/Download/update_hermes_v2.zip ~/hermes/
    cd ~/hermes
    unzip -o update_hermes_v2.zip
    ```

3.  **Primer Inicio**:
    ```bash
    source venv/bin/activate
    python olympus.py
    ```

## 🧠 Integración Panteón

Si el archivo `panteon.py` está presente, Hermes buscará automáticamente un servidor Hestia.

- **Modo Local**: Si existe `hestia.db`, escribe directo en SQL.
- **Modo Remoto**: Si no, intenta contactar a `http://127.0.0.1:5000` (o IP del PC).

## 🛠 Comandos Útiles

- **Ver Logs recientes**: `cat olympus_operations.log | tail -n 20`
- **Empaquetar actualización (en PC)**: `python make_update.py`
