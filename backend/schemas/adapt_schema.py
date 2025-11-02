"""Pydantic schemas for design adaptation API."""
from pydantic import BaseModel
from typing import Optional, List


class ReferenceSummary(BaseModel):
    """Summary of a reference for adaptation."""
    title: str
    url: str
    highlights: List[str]
    assumptions: List[str]
    components: List[str]


class AdaptRequest(BaseModel):
    """Request model for adapting a reference design."""
    user_input: str
    reference: ReferenceSummary
    constraints: Optional[str] = None


class AdaptResponse(BaseModel):
    """Response model for design adaptation."""
    design_markdown: str
    sources: List[str]  # List of source URLs
    changes_summary: str  # Short summary of changes vs source

