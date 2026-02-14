🐦 Myna — Intelligent Data Mining Platform

Myna es una plataforma de data mining diseñada para exploración, limpieza y análisis estadístico de datasets tabulares, con foco en arquitectura escalable, extensibilidad y separación estricta de responsabilidades.

No es un script experimental: es un sistema pensado para crecer en reglas de negocio, algoritmos y usuarios, manteniendo testabilidad y claridad conceptual.

🎯 Problema que resuelve

En muchos entornos analíticos:

Los flujos de análisis viven en notebooks frágiles o scripts monolíticos

La lógica de negocio se mezcla con UI, I/O y visualización

Escalar a múltiples datasets, sesiones o algoritmos implica reescribir todo

Myna ataca ese problema desde la arquitectura, no desde el tooling.

🧠 Enfoque de diseño

Myna está construido bajo Arquitectura Hexagonal (Ports & Adapters), lo que permite:

Aislar el dominio de cualquier framework

Cambiar UI, persistencia o visualización sin tocar la lógica central

Testear el core sin dependencias externas

Evolucionar de herramienta local a servicio multiusuario

✨ Capacidades principales
📊 Análisis y preparación de datos

Estadística descriptiva

Limpieza de datos

Imputación de valores faltantes:

Media

Mediana

Cero

Eliminación

Escalado:

MinMax

Z-Score

Detección y tratamiento de outliers (IQR)

🤖 Aprendizaje no supervisado

K-Means Clustering integrado como servicio de dominio

📈 Visualización interactiva

Gráficos dinámicos con Plotly.js

Zoom, pan y hover

Totalmente desacoplado del core

🏗️ Arquitectura
src/
├── core/ # Dominio puro (sin frameworks)
│ ├── domain_services.py # Estadística, limpieza, clustering
│ ├── models.py # Modelos de dominio (Session, Dataset)
│ └── ports.py # Interfaces (Ports)
│
├── adapters/ # Implementaciones externas
│ ├── api/ # FastAPI (entrada HTTP)
│ │ ├── router.py
│ │ └── dependencies.py # Inyección de dependencias
│ ├── repositories/ # Persistencia (repositorios)
│ ├── fs/ # Acceso a archivos
│ └── visualization/ # Plotting (Plotly)
│
└── main.py # Bootstrap de la aplicación

## ⚖️ Decisiones de Arquitectura (ADR)

Este proyecto toma decisiones técnicas conscientes basadas en restricciones de despliegue real (Capa Gratuita de Vercel / Serverless AWS Lambda):

1.  **Optimización "Zero-Dependencies"**:
    - **Problema**: Límite estricto de 250MB para Serverless Functions. Librerías como `scikit-learn` y `scipy` exceden este límite.
    - **Solución**: Implementación **nativa (NumPy/Pandas Pure)** de algoritmos como K-Means, Z-Score y Fisher Kurtosis. Se eliminaron dependencias pesadas para mantener el artifact ligero (<100MB).

2.  **Persistencia Agnostica**:
    - La arquitectura define interfaces (`ports.py`) que permiten cambiar el almacenamiento de `LocalStorage` (actual, para demos) a `S3/BlobStorage` (producción) cambiando una sola línea de inyección de dependencias.

3.  **Visualización Desacoplada**:
    - Generación de gráficos JSON (Plotly) en el backend, permitiendo que cualquier frontend (React, Vue, Vanilla) renderice la interacción sin lógica de negocio en el cliente.

📌 Regla clave:

El dominio no conoce a FastAPI, Plotly ni al filesystem.
Los adapters dependen del core, nunca al revés.

🧪 Testing

Los tests están enfocados en comportamiento de dominio, no en frameworks.

PYTHONPATH=. pytest tests/

Esto permite refactors estructurales sin romper la lógica central.

▶️ Ejecución

# Crear entorno virtual

python3 -m venv venv
source venv/bin/activate

# Instalar dependencias

pip install -r requirements.txt

# Ejecutar

python src/main.py

Abrir en el navegador:
👉 http://localhost:8000

🔄 Evolución del proyecto

V5.1 — Arquitectura Stateless, Repository Pattern, soporte multi-sesión

V5.0 — Migración completa a FastAPI + UI custom, Hexagonal Architecture

V4.0 — Modularización inicial (Gradio)

Legacy — Script monolítico final_eval3mineria.py

El historial completo de decisiones técnicas y tareas pendientes vive en la Bitácora de Desarrollo (Bitacora.md).

🧭 Visión a futuro

Myna está preparada para evolucionar hacia:

Persistencia real de sesiones

Ejecución concurrente

Nuevos algoritmos plug-and-play

UI desacoplada como cliente independiente

Uso como servicio analítico interno o producto

🧩 Por qué este proyecto importa

Este repositorio no busca mostrar “features”, sino criterio técnico:

Diseño orientado al cambio

Separación estricta de responsabilidades

Dominio como ciudadano de primera clase

## Código escrito para otros desarrolladores

_Created by Medalcode & Team_

## Agent & Skills (extensibilidad)

Se ha añadido una capa de orquestación basada en el concepto de `Agent` y `Skill` para facilitar pipelines reproducibles y extensibles.

- `Agent`: orquestador de alto nivel que coordina la ejecución de skills sobre una `AnalysisSession`.
- `Skill`: acción atómica y registrable que opera sobre la sesión (ej.: `clean_nulls`, `scale_columns`, `kmeans_cluster`).

Implementación inicial en el repo:

- `docs/agent.md` — explicación conceptual y ciclo de vida.
- `docs/skills.md` — catálogo, convenciones y plantilla de skills.
- `src/core/agents/base.py` — `AgentManager`, `SkillResult` y decorador `@register_skill`.
- `src/core/agents/skills/clean_nulls.py` — ejemplo de skill que usa `DataCleaner`.

Motivación: permite agregar nuevas capacidades como plugins (skills) sin cambiar el router ni el core, mejorar trazabilidad y facilitar pruebas.

Notas operativas:

- Para inyectar el manager en rutas, usar `get_agent_manager()` desde `src/adapters/api/dependencies.py`.
- Recomendado añadir `skill_history` y `schema_version` en `AnalysisSession` para auditoría y rollback.

