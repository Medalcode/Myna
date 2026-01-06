# 🔄 Plan de Reformulación Hermes - Versión Limpia

**Fecha:** 2026-01-06  
**Objetivo:** Consolidar Hermes como sistema autónomo, eliminando dependencias rotas

---

## 🗑️ Proyectos Abandonados

Los siguientes proyectos se abandonan y sus referencias se eliminarán:

- ❌ **Hefesto** - Mobile farm (no funcionó bien)
- ❌ **Panoptes** - Scraper (funcionó parcialmente)
- ❌ **Hestia** - Dashboard centralizado (se rompió tras cambios)
- ❌ **Argos** - Trading bot (dependencia externa)
- ❌ **Panteon SDK** - Sistema de integración (innecesario para Hermes standalone)

---

## ✅ Hermes V4.0 - Arquitectura Limpia

### Estructura Final:

```
Hermes/
├── hermes.py              # 🆕 Punto de entrada principal (reemplaza olympus.py)
├── faucet_bot/
│   ├── __init__.py
│   ├── main.py            # Core del bot
│   ├── database.py        # 🆕 Unificado (oracle + hermes_db)
│   ├── config_loader.py
│   ├── config.json        # 🆕 Configuración inicial
│   ├── captcha_solver.py
│   ├── proxy_manager.py
│   ├── proxies.txt
│   ├── requirements.txt
│   ├── recipes/
│   │   ├── __init__.py
│   │   ├── base_recipe.py
│   │   └── cointiply.py
│   └── sessions/
├── logs/
│   └── hermes.log         # 🆕 Logs centralizados
├── data/
│   └── hermes.db          # 🆕 Base de datos SQLite
├── termux_install.sh
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🔧 Cambios Específicos

### 1. Eliminar Archivos Obsoletos

- ❌ `olympus.py` → Reemplazar por `hermes.py` (sin Argos, sin Panteon)
- ❌ `panteon.py` → Eliminar
- ❌ `battery_monitor.py` → Mover a `faucet_bot/utils/` (opcional)
- ❌ `hermes_db.py` → Fusionar con `faucet_bot/database.py`

### 2. Simplificar `hermes.py`

- Solo dashboard de Hermes
- Monitoreo de batería (opcional, solo si está en Termux)
- Estadísticas de la base de datos local
- Sin hilos de Argos ni conexiones a Hestia

### 3. Unificar Base de Datos

- Fusionar `hermes_db.py` y `faucet_bot/database.py` en uno solo
- Esquema único con tablas:
  - `runs` - Registro de ejecuciones
  - `earnings` - Ganancias acumuladas
  - `proxies` - Estado de proxies

### 4. Configuración Inicial

- Crear `faucet_bot/config.json` con valores por defecto
- Wizard interactivo en primer arranque

### 5. Logs Centralizados

- Todo en `logs/hermes.log`
- Formato consistente
- Rotación automática (opcional)

---

## 📋 Checklist de Implementación

- [ ] Crear nueva estructura de directorios (`logs/`, `data/`)
- [ ] Fusionar bases de datos en `faucet_bot/database.py`
- [ ] Crear `hermes.py` simplificado
- [ ] Generar `config.json` inicial
- [ ] Actualizar imports en `faucet_bot/main.py`
- [ ] Limpiar `olympus.py` o eliminarlo
- [ ] Actualizar `README.md` con nueva estructura
- [ ] Actualizar `termux_install.sh`
- [ ] Probar ejecución local
- [ ] Validar en Termux (Motorola)

---

## 🎯 Resultado Esperado

Un bot **simple, robusto y autónomo** que:

- ✅ Se ejecuta con un solo comando: `python3 hermes.py`
- ✅ No depende de servicios externos (Hestia, Panteon)
- ✅ Tiene toda su lógica autocontenida
- ✅ Es fácil de desplegar en Termux
- ✅ Mantiene logs y estadísticas locales
- ✅ Puede escalar a múltiples faucets fácilmente

---

**Próximo paso:** Implementar los cambios en orden
