from pydantic import BaseModel
from typing import Optional, Any

class Observation(BaseModel):
    broken_query: str
    difficulty: str
    result: Optional[Any] = None
    error: Optional[str] = None

class Action(BaseModel):
    query: str