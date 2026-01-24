# 📔 Bitácora de Desarrollo - Myna

Esta bitácora registra el progreso, las decisiones arquitectónicas y las tareas pendientes del proyecto Myna.

## ✅ Tareas Realizadas

### 1. Migración y Arquitectura Base (V5.0)

- [x] **Adopción de Arquitectura Hexagonal**: Separación estricta entre `core` (dominio), `adapters` (infraestructura) y `main` (entrada).
- [x] **Backend con FastAPI**: Reemplazo del script monolítico por una API RESTful moderna y rápida.
- [x] **Frontend Web**: Implementación de una interfaz web propia usando HTML5, CSS3 y Vanilla JS, eliminando la dependencia de Gradio.

### 2. Funcionalidades de Análisis de Datos

- [x] **Carga de Datos**: Soporte para archivos CSV y Excel vía API.
- [x] **Análisis Estadístico**: Cálculo de estadísticas descriptivas (media, mediana, desviación, etc.) y matrices de correlación.
- [x] **Visualización Interactiva**: Gráficos dinámicos con Plotly.js (Mapas de calor, dispersión, histogramas).

### 3. Operaciones de Limpieza (DataOps)

- [x] **Tratamiento de Nulos**: Imputación por media, mediana, cero o eliminación de filas.
- [x] **Escalado de Datos**: Normalización (MinMax) y Estandarización (Z-Score).

### 4. Machine Learning (No Supervisado)

- [x] **Clustering**: Implementación del algoritmo K-Means con selección dinámica de K.
- [x] **Visualización de Clusters**: Gráficos de dispersión coloreados por cluster asignado.

### 5. Refactorización para Escalabilidad (V5.1 - Actual)

- [x] **Eliminación de Estado Global**: Se eliminó la variable global `session` que impedía la concurrencia.
- [x] **Patrón Repository**: Creación de `ports.py` e implementación de `LocalFileSessionRepository` y `LocalFileDataRepository`.
- [x] **Persistencia Eficiente**: Uso de `Parquet` para guardar DataFrames en disco y `JSON` para metadatos de sesión.
- [x] **Inyección de Dependencias**: Implementación de `dependencies.py` para gestionar el ciclo de vida de la sesión por request.
- [x] **Soporte Multi-usuario (Básico)**: Gestión de sesiones mediante Cookies (`session_id`), permitiendo múltiples usuarios simultáneos sin colisiones.

## 📝 Tareas Pendientes (Roadmap)

### Corto Plazo

- [ ] **Tests Unitarios**: Aumentar cobertura de tests para los nuevos repositorios y la capa de dominio.
- [ ] **Dockerización**: Crear `Dockerfile` y `docker-compose.yml` para despliegue contenerizado.
- [ ] **Validación de Tipos**: Mejorar el manejo de errores y validación de esquemas en la carga de archivos.

### Mediano Plazo

- [ ] **Base de Datos Real**: Implementar adaptadores para Redis (Sesiones) y PostgreSQL/S3 (Datos) usando los puertos existentes.
- [ ] **Nuevos Algoritmos**: Agregar Regresión Lineal/Logística y Árboles de Decisión.
- [ ] **Historial de Operaciones**: Visualizar en el frontend el log de cambios realizados al dataset (Deshacer/Rehacer).

### Largo Plazo

- [ ] **Autenticación real**: Integrar OAuth2 o JWT para cuentas de usuario persistentes.
- [ ] **Cola de Tareas**: Integrar Celery/Redis para procesamientos pesados en background (datasets > 1GB).
