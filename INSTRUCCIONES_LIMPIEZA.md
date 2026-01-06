# 🧹 Instrucciones de Limpieza del Teléfono

## 📋 Resumen

Este documento explica cómo limpiar completamente el teléfono Motorola de todos los proyectos rotos (Hestia, Hefesto, Panoptes, Argos) y dejar solo Hermes V4.0 limpio y funcional.

---

## ⚠️ IMPORTANTE - Lee Antes de Ejecutar

### ¿Qué se va a eliminar?

- ❌ **Hestia** - Dashboard roto que no mostraba ni "Hola Mundo"
- ❌ **Hefesto** - Mobile farm con problemas de captchas
- ❌ **Panoptes** - Scraper que solo obtenía datos ficticios
- ❌ **Argos** - Trading bot abandonado
- ❌ **Panteon SDK** - Complejidad innecesaria
- ❌ Archivos obsoletos en Hermes (olympus.py, panteon.py, etc.)
- ❌ Bases de datos antiguas (olympus.db, hestia.db, etc.)

### ¿Qué se va a mantener?

- ✅ **Hermes V4.0** - Único proyecto funcional
- ✅ Configuración de Hermes (si existe)
- ✅ Proxies configurados
- ✅ Sesiones guardadas

---

## 🚀 Método 1: Limpieza Automática (Recomendado)

### Paso 1: Transferir el Script al Teléfono

**Opción A: Via ADB (desde PC)**

```bash
# Conectar el teléfono via USB
adb devices

# Transferir el script
adb push cleanup_phone.sh /sdcard/Download/

# Conectar a Termux
adb shell

# En Termux:
cd ~
cp /sdcard/Download/cleanup_phone.sh .
chmod +x cleanup_phone.sh
```

**Opción B: Via Git (si tienes Hermes en el teléfono)**

```bash
# En Termux:
cd ~/Hermes
git pull  # Si usas git
# O simplemente el script ya debería estar ahí
```

**Opción C: Copiar manualmente**

1. Conecta el teléfono al PC via USB
2. Copia `cleanup_phone.sh` a la carpeta `Download` del teléfono
3. En Termux:

```bash
cd ~
cp /sdcard/Download/cleanup_phone.sh .
chmod +x cleanup_phone.sh
```

### Paso 2: Ejecutar el Script

```bash
# En Termux:
./cleanup_phone.sh
```

El script te pedirá confirmación. Escribe `SI` (en mayúsculas) para continuar.

### Paso 3: Verificar

El script mostrará un resumen de lo que eliminó. Verifica que todo esté correcto.

---

## 🔧 Método 2: Limpieza Manual

Si prefieres hacerlo manualmente o el script falla:

### Paso 1: Detener Procesos

```bash
# En Termux:
pkill -f hestia
pkill -f hefesto
pkill -f panoptes
pkill -f argos
pkill -f cerbero
pkill -f olympus
```

### Paso 2: Eliminar Directorios de Proyectos

```bash
cd ~
rm -rf Hestia
rm -rf Hefesto
rm -rf Panoptes
rm -rf Argos
```

### Paso 3: Limpiar Archivos Obsoletos en Hermes

```bash
cd ~/Hermes

# Eliminar archivos obsoletos
rm -f olympus.py
rm -f panteon.py
rm -f hermes_db.py
rm -f battery_monitor.py
rm -f make_update.py
rm -f debug_import.py
rm -f olympus.db
rm -f olympus_operations.log
rm -f update_hermes*.zip
```

### Paso 4: Limpiar Bases de Datos Antiguas

```bash
cd ~/Hermes
rm -f hestia.db
rm -f panteon.db
```

### Paso 5: Crear Estructura Correcta

```bash
cd ~/Hermes
mkdir -p data
mkdir -p logs
mkdir -p faucet_bot/sessions
```

### Paso 6: Limpiar Caché

```bash
cd ~/Hermes
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
```

---

## ✅ Verificación Post-Limpieza

Después de la limpieza, verifica que Hermes V4.0 esté intacto:

```bash
cd ~/Hermes

# Verificar archivos críticos
ls -la hermes.py                    # Debe existir
ls -la faucet_bot/database.py       # Debe existir
ls -la faucet_bot/config.json       # Debe existir (o se creará)
ls -la start.sh                     # Debe existir

# Verificar directorios
ls -la data/                        # Debe existir
ls -la logs/                        # Debe existir

# Verificar que NO existan archivos obsoletos
ls -la olympus.py 2>/dev/null       # NO debe existir
ls -la panteon.py 2>/dev/null       # NO debe existir
ls -la hestia.db 2>/dev/null        # NO debe existir
```

---

## 🚀 Próximos Pasos Después de la Limpieza

### 1. Configurar Proxies

```bash
cd ~/Hermes
nano faucet_bot/proxies.txt
```

Añade tus proxies (uno por línea):

```
123.45.67.89:8080
user:pass@98.76.54.32:3128
```

### 2. Ejecutar Hermes

```bash
cd ~/Hermes
python hermes.py
```

O usar el script de inicio:

```bash
./start.sh
```

### 3. Verificar que Funciona

- ✅ El wizard de configuración debe aparecer (primera vez)
- ✅ Se debe crear `data/hermes.db`
- ✅ Se deben escribir logs en `logs/hermes.log`
- ✅ El dashboard debe mostrar estadísticas

---

## 🆘 Troubleshooting

### Error: "Permission denied"

```bash
chmod +x cleanup_phone.sh
chmod +x start.sh
chmod +x hermes.py
```

### Error: "No such file or directory"

Verifica que estás en el directorio correcto:

```bash
pwd  # Debe mostrar algo como /data/data/com.termux/files/home/Hermes
```

### Error: "Command not found"

Asegúrate de estar en Termux, no en el shell de Android.

### El script no elimina algo

Hazlo manualmente siguiendo el Método 2.

---

## 📊 Checklist de Limpieza

Marca cada item cuando lo completes:

- [ ] Script transferido al teléfono
- [ ] Script ejecutado con confirmación "SI"
- [ ] Procesos detenidos
- [ ] Directorios eliminados (Hestia, Hefesto, Panoptes, Argos)
- [ ] Archivos obsoletos eliminados de Hermes
- [ ] Bases de datos antiguas eliminadas
- [ ] Estructura de Hermes verificada
- [ ] Caché limpiado
- [ ] Verificación post-limpieza completada
- [ ] Proxies configurados
- [ ] Hermes ejecutado y funcionando

---

## 🎯 Resultado Esperado

Después de la limpieza:

```
~/
├── Hermes/              ✅ ÚNICO PROYECTO
│   ├── hermes.py        ✅ Punto de entrada
│   ├── start.sh         ✅ Script de inicio
│   ├── data/            ✅ Base de datos
│   │   └── hermes.db
│   ├── logs/            ✅ Logs
│   │   └── hermes.log
│   └── faucet_bot/      ✅ Core del bot
│       ├── database.py
│       ├── config.json
│       └── ...
│
├── Hestia/              ❌ ELIMINADO
├── Hefesto/             ❌ ELIMINADO
├── Panoptes/            ❌ ELIMINADO
└── Argos/               ❌ ELIMINADO
```

---

**Última actualización**: 2026-01-06  
**Versión**: 1.0  
**Estado**: Listo para ejecutar
