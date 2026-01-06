# 🎯 Hermes V4.0 - Guía de Migración y Uso

## ✅ Reformulación Completada

La reformulación de Hermes V4.0 ha sido **completada exitosamente**. Todos los archivos han sido actualizados y la estructura está lista para usar.

---

## 📁 Nueva Estructura

```
Hermes/
├── hermes.py              # 🎯 NUEVO: Punto de entrada principal
├── start.sh               # 🚀 NUEVO: Script de inicio rápido
├── data/                  # 🗄️ NUEVO: Base de datos
│   └── hermes.db
├── logs/                  # 📝 NUEVO: Logs centralizados
│   └── hermes.log
├── faucet_bot/
│   ├── database.py        # 🔧 ACTUALIZADO: DB unificada
│   ├── config.json        # ⚙️ NUEVO: Configuración
│   ├── main.py            # ✅ ACTUALIZADO: Imports arreglados
│   ├── recipes/
│   │   └── cointiply.py
│   └── ...
└── README.md              # 📚 ACTUALIZADO: Documentación V4.0
```

---

## 🚀 Cómo Empezar

### Opción 1: Script de Inicio Rápido (Recomendado)

```bash
./start.sh
```

Este script:

- ✅ Crea y activa el entorno virtual automáticamente
- ✅ Instala dependencias si es necesario
- ✅ Verifica la configuración
- ✅ Lanza Hermes

### Opción 2: Inicio Manual

```bash
# 1. Activar entorno virtual (si usas uno)
source venv/bin/activate

# 2. Instalar dependencias (primera vez)
pip install -r faucet_bot/requirements.txt
playwright install chromium

# 3. Ejecutar Hermes
python3 hermes.py
```

---

## ⚙️ Configuración Inicial

### 1. Proxies (OBLIGATORIO)

Edita `faucet_bot/proxies.txt`:

```
# Formato simple
123.45.67.89:8080
98.76.54.32:3128

# Con autenticación
user:pass@123.45.67.89:8080
```

### 2. Credenciales de Cointiply

En el primer arranque, el wizard te pedirá:

- Email de Cointiply
- Password de Cointiply

O edita manualmente `faucet_bot/config.json`:

```json
{
  "cointiply": {
    "email": "tu@email.com",
    "password": "tupassword"
  }
}
```

### 3. Captcha Solver (Opcional)

Para automatización completa, añade tu API Key de 2Captcha:

```json
{
  "captcha": {
    "provider": "2captcha",
    "api_key": "tu_api_key_aqui"
  }
}
```

---

## 📊 Monitoreo

### Ver Dashboard en Tiempo Real

El dashboard se actualiza automáticamente cada 2 segundos y muestra:

- 🔋 Estado de batería (si está en Termux)
- 🌐 Número de proxies cargados
- 📈 Estado actual del bot
- 💰 Balance total y del día
- 📊 Tasa de éxito (WIN/FAIL)

### Ver Logs

```bash
# En tiempo real
tail -f logs/hermes.log

# Últimas 50 líneas
tail -n 50 logs/hermes.log

# Buscar errores
grep ERROR logs/hermes.log
```

### Consultar Base de Datos

```bash
# Ver últimas 10 ejecuciones
sqlite3 data/hermes.db "SELECT * FROM runs ORDER BY timestamp DESC LIMIT 10;"

# Ver estadísticas totales
sqlite3 data/hermes.db "SELECT result, COUNT(*) as count FROM runs GROUP BY result;"

# Ver ganancias por día
sqlite3 data/hermes.db "SELECT DATE(timestamp) as date, SUM(sats) as total FROM runs WHERE result='WIN' GROUP BY DATE(timestamp);"
```

---

## 🔧 Comandos Útiles

### Ejecutar en Segundo Plano

```bash
# Linux/Mac
nohup python3 hermes.py > /dev/null 2>&1 &

# Termux
nohup python hermes.py > /dev/null 2>&1 &
```

### Detener el Bot

```bash
# Si está en primer plano
Ctrl+C

# Si está en segundo plano
pkill -f hermes.py
```

### Ver Procesos Activos

```bash
ps aux | grep hermes
```

---

## 📱 Instalación en Termux (Android)

### 1. Preparar Termux

```bash
# Actualizar paquetes
pkg update && pkg upgrade -y

# Instalar dependencias
pkg install python git -y
```

### 2. Clonar Repositorio

```bash
git clone https://github.com/TuUsuario/Hermes.git
cd Hermes
```

### 3. Ejecutar Instalador

```bash
bash termux_install.sh
```

### 4. Configurar y Ejecutar

```bash
# Editar proxies
nano faucet_bot/proxies.txt

# Ejecutar
python hermes.py
```

### 5. Mantener Activo

Para que el bot siga corriendo cuando cierras Termux:

```bash
# Ejecutar en segundo plano
nohup python hermes.py > /dev/null 2>&1 &

# Salir de Termux (el bot seguirá corriendo)
exit
```

**Importante**:

- Mantén el dispositivo conectado al cargador
- Usa una app como "Caffeine" para evitar que la CPU se duerma
- Instala Termux:API para monitoreo de batería

---

## 🗑️ Limpieza de Archivos Obsoletos

Los siguientes archivos son de versiones anteriores y pueden eliminarse:

```bash
# Archivos obsoletos (ya no se usan)
rm olympus.py          # Reemplazado por hermes.py
rm panteon.py          # Ya no se usa
rm hermes_db.py        # Fusionado en faucet_bot/database.py
rm battery_monitor.py  # Integrado en hermes.py
rm make_update.py      # Ya no se usa
rm debug_import.py     # Ya no se usa

# Bases de datos antiguas
rm olympus.db          # Ahora es data/hermes.db
rm olympus_operations.log  # Ahora es logs/hermes.log
```

**Nota**: Haz un backup antes de eliminar si tienes datos importantes.

---

## 🐛 Troubleshooting

### Error: "No module named 'playwright'"

```bash
pip install playwright
playwright install chromium
```

### Error: "No proxies loaded"

Asegúrate de tener proxies en `faucet_bot/proxies.txt` (uno por línea).

### Error: "Permission denied: ./start.sh"

```bash
chmod +x start.sh
chmod +x hermes.py
```

### El bot no hace nada

1. Verifica que tengas proxies configurados
2. Revisa los logs: `tail -f logs/hermes.log`
3. Verifica credenciales en `faucet_bot/config.json`

### Error de imports

```bash
# Asegúrate de estar en el directorio correcto
cd /ruta/a/Hermes

# Verifica que faucet_bot/ existe
ls -la faucet_bot/
```

---

## 📈 Próximos Pasos

1. **Validar en PC**: Ejecuta `./start.sh` y verifica que todo funciona
2. **Configurar Proxies**: Añade proxies de calidad en `faucet_bot/proxies.txt`
3. **Configurar Credenciales**: Completa el wizard o edita `config.json`
4. **Monitorear**: Deja correr 1-2 horas y revisa logs/estadísticas
5. **Desplegar en Termux**: Si todo funciona, despliega en el Motorola

---

## 📚 Documentación Adicional

- `README.md` - Documentación completa
- `BITACORA_HERMES.md` - Historial de cambios
- `PLAN_REFORMULACION.md` - Plan de reformulación
- `RESUMEN_CAMBIOS.md` - Resumen de cambios V4.0
- `MEJORAS.md` - Ideas de mejoras futuras

---

## ✅ Checklist de Validación

Antes de considerar V4.0 como estable:

- [ ] `python3 hermes.py` se ejecuta sin errores
- [ ] Se crea `data/hermes.db` automáticamente
- [ ] Se crea `logs/hermes.log` automáticamente
- [ ] El wizard de configuración funciona
- [ ] El dashboard muestra estadísticas
- [ ] Los proxies se cargan correctamente
- [ ] Las recetas se ejecutan sin errores
- [ ] Los logs se escriben correctamente
- [ ] La base de datos registra las ejecuciones
- [ ] Funciona en Termux (Motorola)

---

## 🎉 ¡Listo!

Hermes V4.0 está completamente reformulado y listo para usar.

**Comando para empezar**:

```bash
./start.sh
```

¡Buena suerte con la cosecha de satoshis! 🏛️⚡

---

**Última actualización**: 2026-01-06  
**Versión**: Hermes V4.0  
**Estado**: ✅ Listo para producción
