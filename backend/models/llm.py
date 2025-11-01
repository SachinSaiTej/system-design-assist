import ollama
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
import time

load_dotenv()
logger = logging.getLogger(__name__)

class OllamaLLM:
    def __init__(self, model_name="llama2"):
        logger.info(f"🤖 Initializing OllamaLLM with model: {model_name}")
        self.model_name = model_name
        
        try:
            self.client = ollama.Client()
            logger.info("✅ Ollama client created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create Ollama client: {str(e)}")
            self.client = None
        
        # OpenAI fallback
        self.openai_client = None
        if os.getenv("OPENAI_API_KEY"):
            try:
                self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                logger.info("✅ OpenAI client initialized as fallback")
            except Exception as e:
                logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
        else:
            logger.info("ℹ️  No OpenAI API key found, will rely on Ollama only")
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response using Ollama, with OpenAI fallback"""
        
        logger.info("🚀 Starting LLM generation...")
        start_time = time.time()
        
        # Try Ollama first
        logger.info("🔍 Checking Ollama availability...")
        if self.is_ollama_available():
            logger.info("✅ Ollama is available, attempting generation...")
            try:
                messages = []
                
                if system_prompt:
                    messages.append({
                        "role": "system", 
                        "content": system_prompt
                    })
                    logger.info("📋 Added system prompt to messages")
                
                messages.append({
                    "role": "user",
                    "content": prompt
                })
                logger.info(f"💬 Prepared {len(messages)} messages for Ollama")
                
                logger.info(f"🎯 Calling Ollama with model: {self.model_name}")
                ollama_start = time.time()
                
                response = self.client.chat(
                    model=self.model_name,
                    messages=messages,
                    stream=False
                )
                
                ollama_time = time.time() - ollama_start
                logger.info(f"🎉 Ollama responded in {ollama_time:.2f} seconds")
                logger.info(f"📝 Response content length: {len(response['message']['content'])} characters")
                
                return response['message']['content']
                
            except Exception as e:
                ollama_time = time.time() - start_time
                logger.error(f"💥 Ollama error after {ollama_time:.2f} seconds: {str(e)}")
                logger.info("🔄 Falling back to OpenAI...")
        else:
            logger.warning("⚠️  Ollama is not available, checking OpenAI fallback...")
        
        # Try OpenAI fallback
        if self.openai_client:
            logger.info("🌐 Attempting OpenAI generation...")
            try:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                logger.info("📤 Sending request to OpenAI...")
                openai_start = time.time()
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=1500
                )
                
                openai_time = time.time() - openai_start
                logger.info(f"🎉 OpenAI responded in {openai_time:.2f} seconds")
                
                return response.choices[0].message.content
                
            except Exception as e:
                logger.error(f"💥 OpenAI error: {str(e)}")
                return f"OpenAI API error: {str(e)}"
        
        # No LLM available
        logger.warning("⚠️  No LLM available, returning fallback response")
        return self._get_fallback_response()
    
    def is_ollama_available(self) -> bool:
        """Check if Ollama service is running and model is available"""
        logger.info("🔍 Checking if Ollama is available...")
        
        if not self.client:
            logger.warning("⚠️  Ollama client was not initialized")
            return False
            
        try:
            logger.info("📋 Fetching list of available models from Ollama...")
            models = self.client.list()
            
            if not models or 'models' not in models:
                logger.warning("⚠️  No models found in Ollama response")
                return False
                
            model_names = [model['name'] for model in models.get('models', [])]
            logger.info(f"📝 Available models: {model_names}")
            
            is_available = any(self.model_name in name for name in model_names)
            
            if is_available:
                logger.info(f"✅ Model '{self.model_name}' is available in Ollama")
            else:
                logger.warning(f"⚠️  Model '{self.model_name}' not found in available models")
                
            return is_available
            
        except Exception as e:
            logger.error(f"❌ Error checking Ollama availability: {str(e)}")
            logger.error(f"🔍 Error type: {type(e).__name__}")
            return False
    
    def is_model_available(self) -> bool:
        """Check if any LLM (Ollama or OpenAI) is available"""
        return self.is_ollama_available() or self.openai_client is not None
    
    def _get_fallback_response(self) -> str:
        """Provide helpful fallback when no LLM is available"""
        return """🔧 **No LLM Available**

**To use Ollama:**
1. Ensure Ollama is running: `ollama serve`
2. Pull a model: `ollama pull phi` (smaller) or `ollama pull llama2`
3. Restart this backend

**Alternative - Use OpenAI API:**
1. Get an API key from OpenAI
2. Create a `.env` file in the backend directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Restart the backend

**For network issues:**
- Check your internet connection
- Try a different DNS server
- Check if you're behind a corporate firewall"""
