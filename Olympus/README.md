# 🏛️ Olympus V4.0

**Sistema Unificado de Orquestación para Faucet Bots**

Estado: **✅ Producción** (Dashboard + Hermes Worker funcionando)

---

## 📋 Descripción

Olympus V4.0 es un **orquestador modular** que gestiona múltiples bots de faucets desde una única aplicación. Diseñado para correr 24/7 en dispositivos móviles Android (vía Termux + Ubuntu Proot), ofrece:

- 🤖 **Workers modulares** (actualmente: Hermes)
- 📊 **Dashboard Web en tiempo real** (Flask)
- 💾 **Base de datos SQLite centralizada**
- 🔄 **Auto-restart** (próximamente: Watchdog)
- 📱 **Notificaciones Telegram** (roadmap)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│         Olympus Orchestrator            │
├─────────────────┬───────────────────────┤
│  Core Database  │  Dashboard (Flask)    │
│  (olympus.db)   │  Port 5000            │
├─────────────────┴───────────────────────┤
│           Workers Layer                 │
│  ┌─────────────┐  ┌──────────────┐     │
│  │ HermesWorker│  │ Future Bots  │     │
│  │ (Playwright)│  │ (Expandible) │     │
│  └─────────────┘  └──────────────┘     │
└─────────────────────────────────────────┘
```

### Componentes Clave

- **`olympus.py`**: Entry point. Inicia orquestador, dashboard y workers.
- **`core/database.py`**: ORM simple para SQLite (logs, runs, workers).
- **`dashboard.py`**: Servidor Flask para visualización web.
- **`workers/hermes/`**: Bot de faucets (Cointiply, FreeBitcoin, etc.)
- **`web/templates/index.html`**: UI moderna con auto-refresh.

---

## 🚀 Instalación

### En Android (Termux) - Recomendado

**Prerequisitos:**

- Termux (de F-Droid)
- ADB configurado en PC (opcional)

**Pasos:**

```bash
# 1. Instalar proot-distro
pkg install proot-distro -y
proot-distro install ubuntu

# 2. Transferir archivos (desde /sdcard o ADB)
cp /sdcard/olympus_update.tar.gz ~
tar -xzf olympus_update.tar.gz

# 3. Configurar Ubuntu
proot-distro login ubuntu -- bash -c "
    apt update && apt install python3 python3-pip -y &&
    cp -r /data/data/com.termux/files/home/Olympus /root/ &&
    cd /root/Olympus &&
    pip3 install flask --break-system-packages &&
    pip3 install -r workers/hermes/faucet_bot/requirements.txt --break-system-packages &&
    playwright install chromium --with-deps
"
```

### En PC (Linux/Debian)

```bash
cd Olympus
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install -r workers/hermes/faucet_bot/requirements.txt
playwright install chromium
```

---

## 🎮 Uso

### Iniciar Olympus

```bash
# En Termux
proot-distro login ubuntu

# Dentro de Ubuntu
cd /root/Olympus
python3 olympus.py
```

**Salida esperada:**

```
🏛️  OLYMPUS V4.0 - Sistema de Orquestación
============================================================
🚀 Iniciando Olympus...
   Iniciando Dashboard Web (Puerto 5000)...
   Iniciando worker: hermes
✅ Olympus iniciado correctamente
```

### Ver el Dashboard

Abre en tu navegador:

👉 **http://IP_DEL_TELEFONO:5000**

_(Ejemplo: `http://192.168.1.81:5000`)_

El dashboard mostrará:

- ✅ Estado de workers (running/stopped)
- 📈 Últimos runs (WIN/FAIL)
- 📜 Live logs en tiempo real
- 💰 Estadísticas de ganancias

---

## 📊 Estructura de Directorios

```
Olympus/
├── olympus.py              # Entry point
├── dashboard.py            # Flask server
├── core/
│   ├── database.py         # SQLite wrapper
│   └── __init__.py
├── workers/
│   ├── base_worker.py      # Abstract worker class
│   └── hermes/
│       ├── worker.py       # Hermes adapter
│       └── faucet_bot/     # Hermes core logic
├── web/
│   └── templates/
│       └── index.html      # Dashboard UI
├── data/
│   └── olympus.db          # SQLite DB
└── logs/                   # Future: file logs
```

---

## 🛣️ Roadmap

- [x] Arquitectura base
- [x] Base de datos unificada
- [x] Migración de Hermes a Worker
- [x] **Dashboard Web funcional** ✨
- [ ] Watchdog (auto-restart workers)
- [ ] API REST completa
- [ ] Notificaciones Telegram
- [ ] Integración de más bots (FreeBitcoin, etc.)

---

## 🐛 Troubleshooting

**Dashboard no carga:**

- Usa el puerto correcto: `http://IP:5000`
- Verifica firewall (puerto 5000)
- Revisa logs en Termux

**Worker no arranca:**

- Confirma instalación de Playwright/Chromium
- Verifica proxies en `workers/hermes/faucet_bot/proxies.txt`

**Error de permisos (Termux):**

- Ejecuta `termux-setup-storage`

---

**MedalCode** - 2026  
_"Una aplicación, muchos bots"_
