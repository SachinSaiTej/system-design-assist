"""Design generation API endpoints."""
from fastapi import APIRouter, HTTPException
from typing import Optional
import logging
import time

from schemas.design_schema import DesignRequest, DesignResponse
from core.prompt_builder import PromptBuilder
from core.ai_client import AIClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/design", tags=["design"])

# Initialize components
prompt_builder = PromptBuilder()
ai_client = AIClient()


@router.post("/generate", response_model=DesignResponse)
async def generate_design(request: DesignRequest):
    """
    Generate a system design document based on user input.
    
    Args:
        request: DesignRequest containing user_input
        
    Returns:
        DesignResponse with markdown-formatted design document
    """
    start_time = time.time()
    logger.info(f"📨 Received design generation request: '{request.user_input[:100]}...'")
    
    try:
        # Build prompts
        logger.info("📝 Building system and user prompts...")
        system_prompt = prompt_builder.build_system_prompt()
        user_prompt = prompt_builder.build_user_prompt(request.user_input)
        
        # Generate design using AI
        logger.info("🤖 Calling AI client...")
        design_markdown = ai_client.generate(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=3000
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        logger.info(f"✅ Design generated successfully in {processing_time:.2f} seconds")
        logger.info(f"📊 Response length: {len(design_markdown)} characters")
        
        return DesignResponse(design_markdown=design_markdown)
        
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
        logger.error(f"❌ Error generating design after {processing_time:.2f} seconds: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Design generation failed",
                "message": str(e)
            }
        )


