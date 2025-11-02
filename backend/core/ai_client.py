"""AI client abstraction for LLM interactions."""
import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class AIClient:
    """Client for interacting with AI models (OpenAI/Anthropic)."""
    
    def __init__(self):
        """Initialize the AI client with OpenAI or fallback."""
        self.openai_client: Optional[OpenAI] = None
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4")
        
        # Initialize OpenAI if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.openai_client = OpenAI(api_key=api_key)
                logger.info(f"✅ OpenAI client initialized with model: {self.model_name}")
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
        else:
            logger.warning("⚠️  No OPENAI_API_KEY found in environment")
    
    def generate(
        self, 
        user_prompt: str, 
        system_prompt: Optional[str] = None,
        max_tokens: int = 3000
    ) -> str:
        """
        Generate a response from the AI model.
        
        Args:
            user_prompt: The user's prompt/question
            system_prompt: Optional system prompt to guide the AI
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text response from AI
            
        Raises:
            ValueError: If no AI client is available
        """
        if not self.openai_client:
            raise ValueError(
                "No AI client available. Please set OPENAI_API_KEY in your .env file."
            )
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})
        
        logger.info(f"📤 Sending request to OpenAI ({self.model_name})...")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            logger.info(f"✅ Received response ({len(content)} characters)")
            
            return content
            
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {str(e)}")
            raise


