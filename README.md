# Proyecto Hermes: Automatización y Trading

Este proyecto integra dos sistemas automatizados bajo un panel de control unificado "Olympus".

## Estructura

- **Olympus Dashboard (`olympus.py`)**: El panel de control central que coordina y visualiza las operaciones.
- **Hermes (`faucet_bot/`)**: Bot de automatización de faucets con rotación de proxies y stealth.
- **Argos**: (Simulado en Olympus) Bot de trading basado en RSI.

## Instalación

1.  Asegúrate de tener Python instalado.
2.  Prepara el entorno de Hermes:
    ```bash
    cd faucet_bot
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium
    ```

## Ejecución del Dashboard

Para iniciar el sistema unificado "Olympus":

```bash
# Desde la raíz del proyecto
source faucet_bot/venv/bin/activate
python olympus.py
```

## Logs

El sistema genera un registro detallado de todas las operaciones en el archivo `olympus_operations.log`.
Puedes auditar este archivo para ver:

- Análisis de mercado de Argos.
- Rotación de IPs y claims de Hermes.
- Errores y advertencias del sistema.
