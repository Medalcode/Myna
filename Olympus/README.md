# 🏛️ Olympus V4.0

**Sistema Unificado de Orquestación para Faucet Bots**

Estado: **Alpha Funcional** (Hermes integrado como worker)

## 📋 Descripción

Olympus V4.0 es la evolución de la arquitectura de Hermes, consolidando múltiples bots bajo un solo orquestador. A diferencia de versiones anteriores distribuida, Olympus centraliza la gestión de bases de datos, logs y ejecución.

## 🏗️ Arquitectura

```mermaid
graph TD
    A[Olympus Orchestrator] --> B[Core Database]
    A --> C[Hermes Worker]
    A --> D[Dashboard Web (Pendiente)]
    C --> E[Faucet Bot Logic]
    E --> F[Playwright]
    B --> G[olympus.db]
```

### Componentes Principales

- **`olympus.py`**: Orquestador principal. Inicia y monitorea workers.
- **`core/database.py`**: SQLite unificado. Maneja logs, status y resultados.
- **`workers/hermes/`**: El bot Hermes adaptado para funcionar como worker.

## 🚀 Instalación y Uso

### Requisitos
- Python 3.10+
- Playwright

### Instalación

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r workers/hermes/faucet_bot/requirements.txt
playwright install chromium
```

### Ejecución

```bash
python3 olympus.py
```

## 📊 Estructura de Directorios

```
Olympus/
├── olympus.py              # Entry point
├── core/                   # Sistema central
│   ├── database.py         # DB Wrapper
│   └── __init__.py
├── workers/                # Bots (Workers)
│   ├── base_worker.py      # Clase base abstracta
│   └── hermes/             # Hermes V4.0
│       ├── worker.py       # Adaptador
│       └── faucet_bot/     # Lógica core
├── data/                   # Persistencia
│   └── olympus.db
└── logs/                   # Logs unificados
```

## 🛣️ Roadmap

- [x] Arquitectura base creada
- [x] Base de datos unificada
- [x] Migración de Hermes a Worker
- [ ] Dashboard Web (Flask)
- [ ] Watchdog (Auto-restart)
- [ ] Soporte para Telegram

---
**MedalCode** - 2026
