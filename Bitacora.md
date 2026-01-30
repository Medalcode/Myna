Bitacora
📌 Meta

Project: Myna

Owner: Medalcode

Repo: https://github.com/Medalcode/Hermes

Started: 2026-01-20

LastUpdate: 2026-01-30

🧱 Features
[DONE] F-001 — Adopción de Arquitectura Hexagonal

Description: Separación estricta entre `core` (dominio), `adapters` (infraestructura) y `main` (entrada).

Tags: arquitectura, refactor

Completed: 2026-01-24

[DONE] F-002 — Backend con FastAPI

Description: Reemplazo del script monolítico por una API RESTful moderna y rápida.

Tags: backend, fastapi

Completed: 2026-01-24

[DONE] F-003 — Frontend Web

Description: Implementación de una interfaz web propia usando HTML5, CSS3 y Vanilla JS, eliminando la dependencia de Gradio.

Tags: frontend, vanilla-js

Completed: 2026-01-24

[DONE] F-004 — Carga de Datos

Description: Soporte para archivos CSV y Excel vía API.

Tags: data, csv, excel

Completed: 2026-01-24

[DONE] F-005 — Análisis Estadístico

Description: Cálculo de estadísticas descriptivas (media, mediana, desviación, etc.) y matrices de correlación.

Tags: statistics, analysis

Completed: 2026-01-24

[DONE] F-006 — Visualización Interactiva

Description: Gráficos dinámicos con Plotly.js (Mapas de calor, dispersión, histogramas).

Tags: visualization, plotly

Completed: 2026-01-24

[DONE] F-007 — Tratamiento de Nulos

Description: Imputación por media, mediana, cero o eliminación de filas.

Tags: data-cleaning, preprocessing

Completed: 2026-01-24

[DONE] F-008 — Escalado de Datos

Description: Normalización (MinMax) y Estandarización (Z-Score).

Tags: preprocessing, scaling

Completed: 2026-01-24

[DONE] F-009 — Clustering

Description: Implementación del algoritmo K-Means con selección dinámica de K.

Tags: machine-learning, clustering

Completed: 2026-01-24

[DONE] F-010 — Visualización de Clusters

Description: Gráficos de dispersión coloreados por cluster asignado.

Tags: visualization, clustering

Completed: 2026-01-24

[DONE] F-011 — Eliminación de Estado Global

Description: Se eliminó la variable global `session` que impedía la concurrencia.

Tags: refactor, concurrency

Completed: 2026-01-24

[DONE] F-012 — Patrón Repository

Description: Creación de `ports.py` e implementación de `LocalFileSessionRepository` y `LocalFileDataRepository`.

Tags: architecture, patterns

Completed: 2026-01-24

[DONE] F-013 — Persistencia Eficiente

Description: Uso de `Parquet` para guardar DataFrames en disco y `JSON` para metadatos de sesión.

Tags: storage, performance

Completed: 2026-01-24

[DONE] F-014 — Inyección de Dependencias

Description: Implementación de `dependencies.py` para gestionar el ciclo de vida de la sesión por request.

Tags: architecture, dependency-injection

Completed: 2026-01-24

[DONE] F-015 — Soporte Multi-usuario (Básico)

Description: Gestión de sesiones mediante Cookies (`session_id`), permitiendo múltiples usuarios simultáneos sin colisiones.

Tags: security, session

Completed: 2026-01-24

[TODO] F-016 — Tests Unitarios

Description: Aumentar cobertura de tests para los nuevos repositorios y la capa de dominio.

Tags: testing, qa

[TODO] F-017 — Dockerización

Description: Crear `Dockerfile` y `docker-compose.yml` para despliegue contenerizado.

Tags: devops, docker

[TODO] F-018 — Validación de Tipos

Description: Mejorar el manejo de errores y validación de esquemas en la carga de archivos.

Tags: validation, typing

[TODO] F-019 — Base de Datos Real

Description: Implementar adaptadores para Redis (Sesiones) y PostgreSQL/S3 (Datos) usando los puertos existentes.

Tags: database, infra

[TODO] F-020 — Nuevos Algoritmos

Description: Agregar Regresión Lineal/Logística y Árboles de Decisión.

Tags: machine-learning, algorithms

[TODO] F-021 — Historial de Operaciones

Description: Visualizar en el frontend el log de cambios realizados al dataset (Deshacer/Rehacer).

Tags: frontend, ux

[TODO] F-022 — Autenticación real

Description: Integrar OAuth2 o JWT para cuentas de usuario persistentes.

Tags: security, auth

[TODO] F-023 — Cola de Tareas

Description: Integrar Celery/Redis para procesamientos pesados en background (datasets > 1GB).

Tags: backend, scaling
