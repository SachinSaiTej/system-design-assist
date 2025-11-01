from models.llm import OllamaLLM
import logging
import time

logger = logging.getLogger(__name__)

class SystemDesignRAG:
    def __init__(self):
        logger.info("🔧 Initializing SystemDesignRAG...")
        # Use llama2 model that you have installed
        self.llm = OllamaLLM("llama2")  # Your installed model
        logger.info("🧠 LLM initialized with model: llama2")
        
        self.system_prompt = """You are an expert system design engineer. 
        Provide detailed, practical system design solutions including:
        - Architecture diagrams and explanations
        - Database design considerations
        - Scalability strategies
        - Technology stack recommendations
        - Load balancing and caching strategies
        
        Format your response in clear markdown with appropriate headings."""
        
        logger.info("✅ SystemDesignRAG initialization complete!")
    
    def generate(self, question: str) -> str:
        """Generate system design answer using RAG pipeline"""
        
        logger.info(f"🎯 Starting generation for question: '{question[:50]}...'")
        start_time = time.time()
        
        # Enhanced prompt for better system design responses
        enhanced_prompt = f"""
        System Design Question: {question}
        
        Please provide a comprehensive system design solution covering:
        1. High-level architecture
        2. Key components and their interactions
        3. Database design
        4. Scalability considerations
        5. Technology recommendations
        
        Be specific and practical in your recommendations.
        """
        
        logger.info("📝 Enhanced prompt created, sending to LLM...")
        logger.info(f"📏 Prompt length: {len(enhanced_prompt)} characters")
        
        try:
            # The LLM class now handles all availability checks and fallbacks
            response = self.llm.generate(enhanced_prompt, self.system_prompt)
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            logger.info(f"🎉 LLM response received in {generation_time:.2f} seconds")
            logger.info(f"📊 Response length: {len(response)} characters")
            logger.info(f"🔍 Response preview: '{response[:100]}...'")
            
            return response
            
        except Exception as e:
            end_time = time.time()
            generation_time = end_time - start_time
            
            logger.error(f"💥 Error in RAG generation after {generation_time:.2f} seconds: {str(e)}")
            raise e