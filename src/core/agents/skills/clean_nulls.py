from typing import List
from src.core.agents.base import register_skill
from src.core.domain_services import DataCleaner
from src.core.models import AnalysisSession


@register_skill("clean_nulls", description="Trata valores nulos en columnas específicas")
def clean_nulls(session: AnalysisSession, columns: List[str], method: str):
    df_new, affected = DataCleaner.handle_nulls(session.current_df, columns, method)
    session.current_df = df_new
    session.add_log(f"Skill: clean_nulls applied {method} on {columns}")

    preview = []
    if df_new is not None:
        preview = df_new.head(10).fillna("").to_dict(orient="records")

    return {"preview": preview, "affected_count": affected}
