from __future__ import annotations

from dash_extensions.enrich import Input, Output

from rzd_planner.app import app
from rzd_planner.services.knowledge_check_service import (
    KnowledgeBaseRowType,
    KnowledgeCheckService,
)


@app.callback(
    Output("check-knowledge-table-id", "data"),
    Input("check-knowledge-table-upload-trigger", "data"),
)
def preload_knowledge_tbl_callback(_: str) -> list[KnowledgeBaseRowType]:
    """Предзагрузка таблицы с полнотой базы знаний"""

    return KnowledgeCheckService().execute()
