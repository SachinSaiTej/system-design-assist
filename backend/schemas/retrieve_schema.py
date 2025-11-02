"""Pydantic schemas for reference retrieval API."""
from pydantic import BaseModel
from typing import List, Optional


class ReferenceHighlight(BaseModel):
    """Single reference highlight summary."""
    title: str
    url: str
    highlights: List[str]  # 3 bullet points
    assumptions: List[str]
    components: List[str]
    confidence_score: float  # 0.0 to 1.0
    snippet: Optional[str] = None  # Original snippet from search


class RetrieveRefsRequest(BaseModel):
    """Request model for retrieving references."""
    user_input: str
    max_results: int = 5


class RetrieveRefsResponse(BaseModel):
    """Response model for reference retrieval."""
    references: List[ReferenceHighlight]
    query: str

