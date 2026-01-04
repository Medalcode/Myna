# 📱 Guía de Instalación: Hermes en Motorola (Termux)

Sigue estos pasos para transformar tu teléfono en una máquina de hacer dinero.

## Requisitos

1.  Teléfono Android (Android 7.0 o superior).
2.  App **Termux** instalada (Descárgala desde F-Droid, NO desde Play Store, la versión de Play Store es obsoleta).
3.  Cable USB para pasar archivos.

## Pasos

### 1. Preparar los Archivos

Conecta tu móvil al PC y copia toda la carpeta `Hermes` adentro del almacenamiento interno del teléfono (ej: en `Descargas/Hermes`).

### 2. Abrir Termux

Abre la app en el teléfono y da permisos de almacenamiento escribiendo esto y aceptando la alerta:

```bash
termux-setup-storage
```

### 3. Copiar y Ejecutar

En la terminal de Termux, ve a la carpeta donde copiaste los archivos y lanza el instalador:

```bash
# Ir a la carpeta (ejemplo)
cd storage/downloads/Hermes

# Dar permisos de ejecución
chmod +x termux_install.sh

# Ejecutar instalador
./termux_install.sh
```

### 4. Finalizar Instalación

El script te pedirá que ejecutes un último comando para instalar las librerías dentro de Ubuntu. Copia y pega lo que te diga la pantalla (será algo como `proot-distro login... install_inside_ubuntu.sh`).

### 5. ¡A Minar! ⛏️

Una vez termine todo, cada vez que quieras encender el bot, solo abre Termux y escribe:

```bash
./start_hermes.sh
```

El bot correrá en segundo plano. Recuerda mantener el teléfono conectado al cargador y con la pantalla activa (o usa una app como "Caffeine" para que no se duerma la CPU).
