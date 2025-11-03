"""Reference retrieval API endpoint."""
from fastapi import APIRouter, HTTPException
from typing import List
import logging
import time

from schemas.retrieve_schema import RetrieveRefsRequest, RetrieveRefsResponse, ReferenceHighlight
from core.retriever import WebRetriever
from core.summarizer import ReferenceSummarizer
from services.scraper import WebScraper
from core.reference_store import ReferenceStore

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/retrieve_refs", tags=["retrieve"])

# Initialize components
retriever = WebRetriever()
summarizer = ReferenceSummarizer()
scraper = WebScraper()
reference_store = ReferenceStore()


@router.post("", response_model=RetrieveRefsResponse)
async def retrieve_references(request: RetrieveRefsRequest):
    """
    Search the web and summarize top references for a user query.
    
    Args:
        request: RetrieveRefsRequest containing user_input and max_results
        
    Returns:
        RetrieveRefsResponse with list of summarized references
    """
    start_time = time.time()
    logger.info(f"📨 Received reference retrieval request: '{request.user_input[:100]}...'")
    
    try:
        # Check cache first
        cached_refs = reference_store.get(request.user_input)
        if cached_refs:
            logger.info("✅ Returning cached references")
            return RetrieveRefsResponse(
                references=[ReferenceHighlight(**ref) for ref in cached_refs],
                query=request.user_input
            )
        
        # Search the web
        logger.info(f"🔍 Searching web for: {request.user_input}")
        search_results = retriever.search(
            query=request.user_input,
            num_results=request.max_results
        )
        
        if not search_results:
            logger.warning("⚠️  No search results found")
            return RetrieveRefsResponse(
                references=[],
                query=request.user_input
            )
        
        # Summarize each result
        logger.info(f"📝 Summarizing {len(search_results)} references...")
        summarized_refs = []
        
        for result in search_results:
            title = result.get("title", "")
            url = result.get("url", "")
            snippet = result.get("snippet", "")
            
            # Try to scrape full content if snippet is too short
            content = snippet
            if len(snippet) < 200:
                logger.info(f"📥 Scraping content from: {url}")
                scraped_content = scraper.scrape_url(url)
                if scraped_content:
                    content = scraped_content[:2000]  # Limit content length
                else:
                    content = snippet  # Fallback to snippet
            
            # Summarize
            summary = summarizer.summarize(
                title=title,
                url=url,
                content_chunk=content,
                user_query=request.user_input
            )
            
            if summary:
                summary["snippet"] = snippet  # Keep original snippet
                summarized_refs.append(summary)
            else:
                logger.warning(f"⚠️  Failed to summarize: {url}")
        
        # Sort by confidence score (descending)
        summarized_refs.sort(key=lambda x: x.get("confidence_score", 0), reverse=True)
        
        # Cache the results
        reference_store.set(request.user_input, summarized_refs)
        
        # Convert to response models
        references = [ReferenceHighlight(**ref) for ref in summarized_refs]
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        logger.info(f"✅ Retrieved and summarized {len(references)} references in {processing_time:.2f} seconds")
        
        return RetrieveRefsResponse(
            references=references,
            query=request.user_input
        )
        
    except Exception as e:
        end_time = time.time()
        processing_time = end_time - start_time
        logger.error(f"❌ Error retrieving references after {processing_time:.2f} seconds: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Reference retrieval failed",
                "message": str(e)
            }
        )

