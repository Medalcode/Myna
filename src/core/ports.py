from abc import ABC, abstractmethod
from typing import Optional, List
import pandas as pd
from .models import AnalysisSession

class SessionRepository(ABC):
    @abstractmethod
    def get_session(self, session_id: str) -> Optional[AnalysisSession]:
        """Retrieves a session metadata by ID."""
        pass

    @abstractmethod
    def save_session(self, session: AnalysisSession) -> None:
        """Saves session metadata."""
        pass

class DataRepository(ABC):
    @abstractmethod
    def save_dataframe(self, session_id: str, df: pd.DataFrame) -> None:
        """Persists the dataframe for a given session."""
        pass

    @abstractmethod
    def load_dataframe(self, session_id: str) -> Optional[pd.DataFrame]:
        """Loads the dataframe for a given session."""
        pass
