from fastapi import Request, Cookie, Response, Depends
import uuid
from src.core.models import AnalysisSession
from src.adapters.repositories.local_storage import LocalFileSessionRepository, LocalFileDataRepository
from src.core.agents.base import AgentManager

# Singleton instances (in a real app, use a proper DI container)
session_repo = LocalFileSessionRepository()
data_repo = LocalFileDataRepository()
# Agent manager singleton (registro inicial de skills se realiza por decorador)
agent_manager = AgentManager()

async def get_session_id(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id)
    return session_id

async def get_analysis_session(session_id: str = Depends(get_session_id)) -> AnalysisSession:
    # Load metadata
    session = session_repo.get_session(session_id)
    if not session:
        session = AnalysisSession()
    
    # Load heavy data
    df = data_repo.load_dataframe(session_id)
    if df is not None:
        session.current_df = df
        
    return session

def save_analysis_session(session_id: str, session: AnalysisSession):
    session_repo.save_session(session, session_id)
    if session.current_df is not None:
        data_repo.save_dataframe(session_id, session.current_df)


def get_agent_manager():
    return agent_manager
