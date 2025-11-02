"""Pydantic schemas for design refinement API."""
from pydantic import BaseModel
from typing import Optional


class RefineRequest(BaseModel):
    """Request model for design refinement."""
    previous_design: str
    instruction: str
    session_id: Optional[str] = None


class RefineResponse(BaseModel):
    """Response model for design refinement."""
    refined_design: str
    session_id: str

