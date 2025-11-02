"""Design refinement API endpoints."""
from fastapi import APIRouter, HTTPException
import logging
import time

from schemas.refine_schema import RefineRequest, RefineResponse
from core.prompt_builder import PromptBuilder
from core.ai_client import AIClient
from core.context_manager import ContextManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/refine", tags=["refine"])

# Initialize components
prompt_builder = PromptBuilder()
ai_client = AIClient()
context_manager = ContextManager()


@router.post("", response_model=RefineResponse)
async def refine_design(request: RefineRequest):
    """
    Refine an existing design document based on new instructions.
    
    Args:
        request: RefineRequest containing previous_design, instruction, and optional session_id
        
    Returns:
        RefineResponse with refined design markdown and session_id
    """
    start_time = time.time()
    logger.info(f"📨 Received design refinement request")
    
    try:
        # Build refinement prompt
        logger.info("📝 Building refinement prompt...")
        system_prompt = prompt_builder.build_system_prompt()
        user_prompt = prompt_builder.build_refinement_prompt(
            previous_design=request.previous_design,
            instruction=request.instruction
        )
        
        # Generate refined design using AI
        logger.info("🤖 Calling AI client for refinement...")
        refined_design = ai_client.generate(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            max_tokens=4000
        )
        
        # Get or create session
        session_id = context_manager.get_or_create_session(
            base_prompt=request.instruction,
            design=refined_design,
            session_id=request.session_id
        )
        
        # Update session with refined design
        context_manager.update_session(
            session_id=session_id,
            updated_design=refined_design,
            add_to_history=True
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        logger.info(f"✅ Design refined successfully in {processing_time:.2f} seconds")
        logger.info(f"📊 Response length: {len(refined_design)} characters")
        logger.info(f"🆔 Session ID: {session_id}")
        
        return RefineResponse(
            refined_design=refined_design,
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
        logger.error(f"❌ Error refining design after {processing_time:.2f} seconds: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Design refinement failed",
                "message": str(e)
            }
        )

