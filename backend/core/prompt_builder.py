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
- Consider real-world constraints and trade-offs
- Format your response in clear markdown with appropriate headings
- Provide actionable, implementation-ready guidance

### Diagrams (IMPORTANT)
You MUST include at least one Mermaid diagram in your response to visualize the architecture or data flow.
Use Mermaid code blocks in the following format:

```mermaid
graph TD
    A[Component A] --> B[Component B]
    B --> C[Component B]
```

Include diagrams in relevant sections such as:
- High-Level Architecture section: Show system components and their relationships
- Data Flow section: Show how data moves through the system
- Component Descriptions: Show interactions between components

Example diagram types to use:
- Flowcharts (graph TD or graph LR) for architecture
- Sequence diagrams for request flows
- State diagrams for state machines
- Class diagrams for component relationships

DO NOT use text descriptions like "see diagram below" - always include the actual Mermaid code block.

### Response
Return structured Markdown from the model without additional JSON wrapping."""

    @staticmethod
    def build_refinement_prompt(previous_design: str, instruction: str) -> str:
        """
        Build a prompt for refining an existing design.
        
        Args:
            previous_design: The previous version of the design
            instruction: New instruction for refinement
            
        Returns:
            Formatted prompt string
        """
        return f"""### Context
{previous_design}

### New Instruction
{instruction}

### Task
Update only relevant sections while keeping existing structure consistent.
Maintain the overall document structure and format. Only modify sections that need to change based on the new instruction.
Ensure consistency with the rest of the document.

### Instructions
- Update the design document based on the new instruction
- Keep unchanged sections intact
- Maintain markdown formatting and structure
- Use Mermaid diagrams where helpful (```mermaid ... ```)
- Ensure the updated design is complete and coherent

### Response
Return the complete updated Markdown document without additional JSON wrapping."""

    @staticmethod
    def build_section_regeneration_prompt(
        previous_design: str, 
        section_name: str, 
        instruction: str
    ) -> str:
        """
        Build a prompt for regenerating a specific section.
        
        Args:
            previous_design: The full previous design document
            section_name: Name of the section to regenerate
            instruction: Instruction for section regeneration
            
        Returns:
            Formatted prompt string
        """
        return f"""### Context
Full system design:
{previous_design}

### Section to Update
{section_name}

### Instruction
{instruction}

### Task
Regenerate only the specified section in Markdown format.
Keep the section consistent with the overall design document style and structure.
Ensure the regenerated section integrates well with the rest of the document.

### Instructions
- Regenerate ONLY the section: {section_name}
- Maintain consistency with the rest of the document
- Use appropriate markdown formatting
- Include Mermaid diagrams if helpful (```mermaid ... ```)
- Return only the regenerated section content, not the entire document

### Response
Return only the regenerated section in Markdown format, maintaining proper heading level for the section."""


