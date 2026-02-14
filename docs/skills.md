# Skills — Catálogo y convenciones

## ¿Qué es una Skill?

Una `Skill` es una acción atómica y reutilizable que opera sobre una `AnalysisSession` o datos relacionados. Debe ser lo más stateless posible y, de preferencia, idempotente.

## Convenciones de implementación

- Firma recomendada: `skill(session: AnalysisSession, **kwargs) -> dict | SkillResult`
- `SkillResult` (recomendado): `{ "changes": {...}, "preview": {...}, "logs": [...] }`
- Las skills deben añadir entradas al log de la `session` para trazabilidad.

## Registro y descubrimiento

- Modo inicial: registro explícito mediante decorador `@register_skill("skill_id")` en `src/core/agents/base.py`.
- Futuro: discovery por entrypoints si se empaqueta el proyecto.

## Catálogo inicial (sugerido)

- I/O
  - `load_file` — cargar un archivo a la sesión (ver `src/adapters/fs/file_io.py`).
  - `export_file` — exportar DataFrame.

- Cleaning
  - `clean_nulls` — tratar valores nulos (implementación de ejemplo en `src/core/agents/skills/clean_nulls.py`).
  - `drop_duplicates`

- Transform
  - `scale_columns` — normalización/estandarización (usa `DataScaler`).
  - `encode_categoricals`

- Stats
  - `compute_descriptive` — retorna summary (usa `StatisticalAnalyzer`).
  - `compute_correlation`

- ML
  - `kmeans_cluster` — delega a `Clusterer.kmeans`.

- Visualization
  - `plot_distribution`, `plot_correlation` — generan objetos de `plotly` (ver `src/adapters/visualization/plotter.py`).

## Plantilla de skill (ejemplo)

```
skill_id: clean_nulls
descripcion: Trata valores nulos en columnas dadas.
signature: clean_nulls(session: AnalysisSession, columns: List[str], method: str) -> dict
outputs: { preview: List[Dict], affected_count: int }
```

## Buenas prácticas

- Mantener efectos laterales explícitos (modificar `session` deliberadamente).
- Añadir pruebas unitarias para cada skill (mock de `AnalysisSession` y repositorios).
- Registrar `skill_history` en la sesión con metadatos para permitir auditoría y rollback.

## Referencias

- Ejemplo de skill: `src/core/agents/skills/clean_nulls.py`
- Registro / manager: `src/core/agents/base.py`
