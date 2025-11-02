"""Section regeneration API endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Tuple
import logging
import time
import re

from schemas.section_schema import SectionRequest, SectionResponse
from core.prompt_builder import PromptBuilder
from core.ai_client import AIClient
from core.context_manager import ContextManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/section", tags=["section"])

# Initialize components
prompt_builder = PromptBuilder()
ai_client = AIClient()
context_manager = ContextManager()


def extract_section_from_markdown(markdown: str, section_name: str) -> Tuple[str, str, str]:
    """
    Extract a section from markdown and return (before, section, after).
    
    Args:
        markdown: Full markdown document
        section_name: Name of section to extract
        
    Returns:
        Tuple of (content_before_section, section_content, content_after_section)
    """
    # Normalize section name for matching (handle various heading formats)
    section_patterns = [
        rf"^#+\s*{re.escape(section_name)}\s*$",
        rf"^#+\s*{re.escape(section_name.replace(' ', '\\s+'))}\s*$",
    ]
    
    lines = markdown.split('\n')
    section_start = -1
    section_end = -1
    current_level = 0
    
    # Find section start
    for i, line in enumerate(lines):
        for pattern in section_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                section_start = i
                # Determine heading level
                current_level = len(line) - len(line.lstrip('#'))
                break
        if section_start != -1:
            break
    
    if section_start == -1:
        # Try fuzzy match
        for i, line in enumerate(lines):
            if section_name.lower() in line.lower() and line.strip().startswith('#'):
                section_start = i
                current_level = len(line) - len(line.lstrip('#'))
                break
    
    if section_start == -1:
        logger.warning(f"⚠️  Section '{section_name}' not found, returning empty section")
        return (markdown, "", "")
    
    # Find section end (next heading of same or higher level, or end of document)
    section_end = len(lines)
    for i in range(section_start + 1, len(lines)):
        line = lines[i].strip()
        if line.startswith('#'):
            heading_level = len(line) - len(line.lstrip('#'))
            if heading_level <= current_level:
                section_end = i
                break
    
    before_section = '\n'.join(lines[:section_start])
    section_content = '\n'.join(lines[section_start:section_end])
    after_section = '\n'.join(lines[section_end:])
    
    return (before_section, section_content, after_section)


def merge_section_into_design(before: str, new_section: str, after: str) -> str:
    """
    Merge a regenerated section back into the full design.
    
    Args:
        before: Content before the section
        new_section: New section content
        after: Content after the section
        
    Returns:
        Complete merged markdown
    """
    parts = []
    if before.strip():
        parts.append(before.strip())
    if new_section.strip():
        parts.append(new_section.strip())
    if after.strip():
        parts.append(after.strip())
    
    return '\n\n'.join(parts)


@router.post("", response_model=SectionResponse)
async def regenerate_section(request: SectionRequest):
    """
    Regenerate a specific section of a design document.
    
    Args:
        request: SectionRequest containing previous_design, section_name, instruction, and optional session_id
        
    Returns:
        SectionResponse with updated design, regenerated section, and session_id
    """
    start_time = time.time()
    logger.info(f"📨 Received section regeneration request for: '{request.section_name}'")
    
    try:
        # Build section regeneration prompt
        logger.info(f"📝 Building section regeneration prompt for '{request.section_name}'...")
        system_prompt = prompt_builder.build_system_prompt()
        user_prompt = prompt_builder.build_section_regeneration_prompt(
            previous_design=request.previous_design,
            section_name=request.section_name,
            instruction=request.instruction
        )
        
        # Generate regenerated section using AI
        logger.info("🤖 Calling AI client for section regeneration...")
        regenerated_section = ai_client.generate(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=2000
        )
        
        # Extract section boundaries and merge
        logger.info("🔗 Merging regenerated section into design...")
        before, _, after = extract_section_from_markdown(
            request.previous_design, 
            request.section_name
        )
        
        updated_design = merge_section_into_design(
            before=before,
            new_section=regenerated_section,
            after=after
        )
        
        # Get or create session
        session_id = context_manager.get_or_create_session(
            base_prompt=request.instruction,
            design=updated_design,
            session_id=request.session_id
        )
        
        # Update session with updated design
        context_manager.update_session(
            session_id=session_id,
            updated_design=updated_design,
            add_to_history=True
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        logger.info(f"✅ Section regenerated successfully in {processing_time:.2f} seconds")
        logger.info(f"📊 Updated design length: {len(updated_design)} characters")
        logger.info(f"🆔 Session ID: {session_id}")
        
        return SectionResponse(
            updated_design=updated_design,
            regenerated_section=regenerated_section,
            session_id=session_id
        )
        
    except ValueError as e:
        end_time = time.time()
        processing_time = end_time - start_time
        logger.error(f"❌ Configuration error after {processing_time:.2f} seconds: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "AI service unavailable",
                "message": str(e),
                "hint": "Please configure OPENAI_API_KEY in your .env file"
            }
        )
        
    except Exception as e:
        end_time = time.time()
        processing_time = end_time - start_time
        logger.error(f"❌ Error regenerating section after {processing_time:.2f} seconds: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Section regeneration failed",
                "message": str(e)
            }
        )

