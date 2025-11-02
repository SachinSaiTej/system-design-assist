"""Markdown-based prompt builder for system design generation."""
from typing import Optional


class PromptBuilder:
    """Builds structured markdown prompts for AI system design generation."""
    
    @staticmethod
    def build_system_prompt() -> str:
        """Build the system prompt for the AI."""
        return """You are an expert software architect with years of experience designing scalable, robust systems.
Your expertise includes distributed systems, microservices architecture, database design, caching strategies, 
load balancing, and system scalability."""

    @staticmethod
    def build_user_prompt(user_input: str) -> str:
        """Build the user prompt with structured output format."""
        return f"""### Task
{user_input}

### Output Format
Provide a complete system design document with the following sections:
1. Functional Requirements
2. Non-Functional Requirements
3. High-Level Architecture
4. Component Descriptions
5. Data Flow
6. Technology Stack Recommendations
7. Scalability & Trade-offs
8. Future Enhancements

### Instructions
- Be specific and practical in your recommendations
- Include diagrams descriptions where relevant (using markdown format)
- Consider real-world constraints and trade-offs
- Format your response in clear markdown with appropriate headings
- Provide actionable, implementation-ready guidance

### Response
Return structured Markdown from the model without additional JSON wrapping."""


