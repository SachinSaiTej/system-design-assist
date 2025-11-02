"""Pydantic schemas for design API requests and responses."""
from pydantic import BaseModel


class DesignRequest(BaseModel):
    """Request model for design generation."""
    user_input: str


class DesignResponse(BaseModel):
    """Response model for design generation."""
    design_markdown: str


