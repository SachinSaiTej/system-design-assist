from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import SystemDesignRAG
import logging
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system_design_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

logger.info("🚀 Initializing System Design RAG...")
rag = SystemDesignRAG()
logger.info("✅ System Design RAG initialized successfully!")

class Query(BaseModel):
    question: str

@app.post("/design")
async def design(q: Query):
    start_time = time.time()
    logger.info(f"📨 Received design request: '{q.question[:100]}...'")
    
    try:
        logger.info("🔄 Processing request with RAG pipeline...")
        answer = rag.generate(q.question)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        logger.info(f"✅ Request processed successfully in {processing_time:.2f} seconds")
        logger.info(f"📤 Response length: {len(answer)} characters")
        
        return {"answer": answer}
    
    except Exception as e:
        end_time = time.time()
        processing_time = end_time - start_time
        
        logger.error(f"❌ Error processing request after {processing_time:.2f} seconds: {str(e)}")
        logger.error(f"🔍 Error type: {type(e).__name__}")
        
        return {"answer": f"Error: {str(e)}"}

@app.get("/health")
async def health_check():
    logger.info("🏥 Health check requested")
    return {"status": "healthy", "message": "System Design Assistant is running!"}
