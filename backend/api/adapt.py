"""Design adaptation API endpoint."""
from fastapi import APIRouter, HTTPException
import logging
import time
import re

from schemas.adapt_schema import AdaptRequest, AdaptResponse
from core.prompt_builder import PromptBuilder
from core.ai_client import AIClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/adapt", tags=["adapt"])

# Initialize components
prompt_builder = PromptBuilder()
ai_client = AIClient()


@router.post("", response_model=AdaptResponse)
async def adapt_design(request: AdaptRequest):
    """
    Adapt a chosen reference design using the main LLM.
    
    Args:
        request: AdaptRequest containing user_input, reference, and constraints
        
    Returns:
        AdaptResponse with adapted design, sources, and changes summary
    """
    start_time = time.time()
    logger.info(f"📨 Received adaptation request for: '{request.user_input[:100]}...'")
    
    try:
        # Convert reference to dict format expected by prompt builder
        reference_summary = {
            "title": request.reference.title,
            "url": request.reference.url,
            "highlights": request.reference.highlights,
            "assumptions": request.reference.assumptions,
            "components": request.reference.components
        }
        
        # Build adaptation prompt
        logger.info("📝 Building adaptation prompt...")
        system_prompt = prompt_builder.build_system_prompt()
        user_prompt = prompt_builder.build_adaptation_prompt(
            user_input=request.user_input,
            reference_summaries=[reference_summary],
            constraints=request.constraints
        )
        
        # Generate adapted design
        logger.info("🤖 Calling AI client for adaptation...")
        design_markdown = ai_client.generate(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=4000
        )
        
        # Extract sources and changes summary from the markdown
        sources = [request.reference.url]  # Base source
        changes_summary = ""
        
        # Try to extract Sources section
        sources_match = re.search(r'##\s+Sources\s*\n(.*?)(?=\n##|\Z)', design_markdown, re.DOTALL | re.IGNORECASE)
        if sources_match:
            sources_text = sources_match.group(1)
            # Extract URLs from sources section
            url_pattern = r'https?://[^\s\)]+'
            found_urls = re.findall(url_pattern, sources_text)
            if found_urls:
                sources.extend(found_urls)
                # Remove duplicates while preserving order
                seen = set()
                sources = [url for url in sources if not (url in seen or seen.add(url))]
        
        # Try to extract Changes vs Source section
        changes_match = re.search(
            r'##\s+Changes\s+vs\s+Source\s*\n(.*?)(?=\n##|\Z)', 
            design_markdown, 
            re.DOTALL | re.IGNORECASE
        )
        if changes_match:
            changes_summary = changes_match.group(1).strip()
        else:
            # If not found, try alternative patterns
            changes_match = re.search(
                r'##\s+Changes\s*\n(.*?)(?=\n##|\Z)', 
                design_markdown, 
                re.DOTALL | re.IGNORECASE
            )
            if changes_match:
                changes_summary = changes_match.group(1).strip()
        
        # If still not found, generate a simple summary
        if not changes_summary:
            changes_summary = "This design was adapted from the reference source with modifications based on the user's specific requirements."
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        logger.info(f"✅ Design adapted successfully in {processing_time:.2f} seconds")
        logger.info(f"📊 Response length: {len(design_markdown)} characters")
        
        return AdaptResponse(
            design_markdown=design_markdown,
            sources=sources,
            changes_summary=changes_summary
        )
        
    except ValueError as e:
        # AI client not available
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
        logger.error(f"❌ Error adapting design after {processing_time:.2f} seconds: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Design adaptation failed",
                "message": str(e)
            }
        )

