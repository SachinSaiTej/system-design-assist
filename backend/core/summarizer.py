"""LLM-based summarizer for web references."""
import json
import logging
from typing import Dict, List, Optional
from core.ai_client import AIClient

logger = logging.getLogger(__name__)


class ReferenceSummarizer:
    """Summarizes web references using LLM."""
    
    def __init__(self):
        """Initialize the summarizer."""
        self.ai_client = AIClient()
    
    def summarize(
        self, 
        title: str, 
        url: str, 
        content_chunk: str,
        user_query: str
    ) -> Optional[Dict]:
        """
        Summarize a reference into structured format.
        
        Args:
            title: Reference title
            url: Reference URL
            content_chunk: Content excerpt from the reference
            user_query: Original user query for context
            
        Returns:
            Dictionary with title, url, highlights, assumptions, components, confidence_score
        """
        prompt = f"""You are a summarizer for system design references.

### Input
Title: {title}
URL: {url}
Content excerpt: {content_chunk[:2000]}  # Limit content length
User Query: {user_query}

### Task
Analyze this reference and extract:
1. 3 key highlights (bullet points) - main insights or design patterns
2. Assumptions made in the design (if any)
3. Key components mentioned
4. Confidence score (0.0 to 1.0) - how relevant this is to the user query

### Output Format
Return ONLY valid JSON in this exact format:
{{
  "title": "...",
  "url": "...",
  "highlights": ["highlight 1", "highlight 2", "highlight 3"],
  "assumptions": ["assumption 1", ...],
  "components": ["component 1", ...],
  "confidence_score": 0.85
}}

### Rules
- Highlights should be concise and actionable
- List components mentioned in the reference
- Confidence score should reflect relevance to user query (higher = more relevant)
- If content is not relevant, set confidence_score < 0.3
- Return ONLY the JSON, no markdown formatting or additional text"""

        try:
            response = self.ai_client.generate(
                user_prompt=prompt,
                system_prompt="You are an expert at analyzing system design references and extracting structured information.",
                max_tokens=1000
            )
            
            # Clean response - remove markdown code blocks if present
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            # Parse JSON
            data = json.loads(response)
            
            # Validate required fields
            required_fields = ["title", "url", "highlights", "assumptions", "components", "confidence_score"]
            for field in required_fields:
                if field not in data:
                    logger.warning(f"Missing field {field} in summary response")
                    if field == "highlights":
                        data[field] = []
                    elif field in ["assumptions", "components"]:
                        data[field] = []
                    elif field == "confidence_score":
                        data[field] = 0.5
            
            # Ensure highlights has exactly 3 items
            highlights = data.get("highlights", [])
            if len(highlights) < 3:
                highlights.extend([""] * (3 - len(highlights)))
            data["highlights"] = highlights[:3]
            
            # Ensure confidence_score is float between 0 and 1
            confidence = float(data.get("confidence_score", 0.5))
            data["confidence_score"] = max(0.0, min(1.0, confidence))
            
            logger.info(f"✅ Successfully summarized: {title}")
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse JSON from summarizer: {str(e)}")
            logger.error(f"Response was: {response[:500]}")
            # Return fallback summary
            return {
                "title": title,
                "url": url,
                "highlights": [content_chunk[:100] if content_chunk else "No highlights available"],
                "assumptions": [],
                "components": [],
                "confidence_score": 0.5
            }
        except Exception as e:
            logger.error(f"❌ Error summarizing reference: {str(e)}")
            return None

