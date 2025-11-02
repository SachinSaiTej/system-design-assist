"""Pydantic schemas for section regeneration API."""
from pydantic import BaseModel
from typing import Optional


class SectionRequest(BaseModel):
    """Request model for section regeneration."""
    previous_design: str
    section_name: str
    instruction: str
    session_id: Optional[str] = None


class SectionResponse(BaseModel):
    """Response model for section regeneration."""
    updated_design: str
    regenerated_section: str
    session_id: str

