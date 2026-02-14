# Agent — Coordinador de Skills

## Propósito

Un `Agent` es el orquestador de alto nivel que coordina la ejecución de `skills` (acciones atómicas) sobre una `AnalysisSession`. Su responsabilidad es planificar, validar, ejecutar y persistir el resultado de una secuencia de skills en un contexto de sesión.

## Arquitectura (visión general)

- Frontend / API → `AgentManager` → `Skill` (acción) → `AnalysisSession` → Repositorios
- `Agent` debe ser ligero, idempotente en lo posible, con historial de acciones para trazabilidad.

```
Client -> API (router) -> AgentManager.execute_skill(...) -> Skill -> Domain Services -> Repos
```

## Modelos y contratos

- `AnalysisSession` (ver `src/core/models.py`): objeto que contiene `current_df` y `logs`.
- Firma esperada para skills: `skill(session: AnalysisSession, **kwargs) -> dict | SkillResult`

## Ciclo de vida de una petición

1. Cliente envía petición (p. ej. `/api/clean/nulls`).
2. Router obtiene `AnalysisSession` (ver `src/adapters/api/dependencies.py`).
3. Router pide al `AgentManager` que ejecute la skill requerida.
4. `AgentManager` valida, ejecuta la skill registrada y devuelve `SkillResult`.
5. Router persiste `AnalysisSession` y devuelve respuesta al cliente.

## Ejemplo de agente (conceptual)

- `DataPrepAgent` — responsabilidades:
  - Validar inputs.
  - Orquestar: `load_file` -> `clean_nulls` -> `scale_columns` -> `save`.
  - Registrar `skill_history` en la sesión (recomendado).

## Trazabilidad y versionado

- Recomendado: extender `AnalysisSession` con `skill_history: List[dict]` y `schema_version: str`.
- Cada skill debe anotar su ejecución en `skill_history` con `skill_id`, `params`, `timestamp` y `result_summary`.

## Operación y despliegue

- En entornos serverless (Vercel) evitar dependencias a estado local compartido; en producción usar S3/DB para `current_df`/artifacts.
- Documentar límites: uso de `/tmp` en Vercel y concurrencia limitada.

## Hooks y extensibilidad

- `AgentManager` puede implementar hooks pre/post (validación, métricas, tracing).
- Discovery de skills: escaneo de `src/core/agents/skills/` o entrypoints (future).

## Referencias

- `src/core/models.py` — `AnalysisSession`
- `src/adapters/api/dependencies.py` — carga/guardado de sesión
- `src/core/domain_services.py` — servicios de dominio que usan las skills
