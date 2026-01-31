# Backlog Técnico & Roadmap

Este documento centraliza la planificación técnica del proyecto Myna. Las tareas están priorizadas por impacto en la estabilidad y escalabilidad del sistema.

## 🔴 High Priority: Estabilización y Persistencia

### [Infra] Implementar Adaptador de S3 para Persistencia Real

**Tipo:** `architecture`, `bug`
**Contexto:** Actualmente, el sistema utiliza `LocalFileSessionRepository` apuntando a `/tmp` en entornos Vercel. Esto causa pérdida de sesión entre despliegues o reinicios de lambdas.
**Criterios de Aceptación:**

- [ ] Crear `S3SessionRepository` y `S3DataRepository` implementando las interfaces de `ports.py`.
- [ ] Configurar inyección de dependencias basada en variables de entorno (`STORAGE_TYPE=s3`).
- [ ] Validar carga y descarga de DataFrames (Pickle/Parquet) desde un bucket privado.

### [Core] Implementar Patrón Strategy para Limpieza y Escalado

**Tipo:** `refactor`, `clean-code`
**Contexto:** `DataCleaner.handle_nulls` y `DataScaler` utilizan cadenas de `if/else` basadas en strings mágicos. Esto viola el principio Open/Closed (OCP).
**Criterios de Aceptación:**

- [ ] Definir interfaz `CleaningStrategy` y `ScalingStrategy`.
- [ ] Implementar clases concretas (`MeanImputation`, `DropRows`, `MinMaxScaling`).
- [ ] Refactorizar servicios de dominio para recibir la estrategia inyectada o seleccionada por Factory.

## 🟡 Medium Priority: Robustez

### [Testing] Test de Integración de Flujo de Sesión

**Tipo:** `tests`, `qa`
**Contexto:** Los tests actuales son unitarios y aislados. No existe garantía de que una sesión persista correctamente tras múltiples operaciones secuenciales.
**Criterios de Aceptación:**

- [ ] Implementar test que simule un ciclo completo: `Upload -> Clean -> Scale -> Cluster -> Stats`.
- [ ] Verificar integridad de datos en cada paso.
- [ ] Validar recuperación de sesión fallida.

### [UX/API] Manejo Asíncrono de Procesos Pesados

**Tipo:** `enhancement`, `scalability`
**Contexto:** Operaciones como Clustering en datasets grandes (>50k filas) pueden causar timeouts HTTP (Gateway Timeout 504).
**Criterios de Aceptación:**

- [ ] Implementar patrón "Job Queue" (endpoint retorna `202 Accepted` + `job_id`).
- [ ] Endpoint de Polling `/api/jobs/{id}/status`.
- [ ] (Opcional) UI con indicador de progreso real.

## 🟢 Future / Low Priority

### [Core] Soporte para DuckDB

**Tipo:** `performance`
**Contexto:** Cargar todo el DataFrame en memoria RAM con Pandas es ineficiente para datasets grandes.
**Propuesta:** Usar DuckDB como motor de consulta SQL sobre archivos locales/S3 para operaciones de agregación sin carga total en memoria.
