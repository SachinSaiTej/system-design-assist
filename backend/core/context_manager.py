"""Session context management for design iterations."""
import uuid
from typing import Dict, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SessionContext:
    """Represents a design session context."""
    
    def __init__(self, session_id: str, base_prompt: str, latest_design: str):
        self.session_id = session_id
        self.base_prompt = base_prompt
        self.latest_design = latest_design
        self.history: List[str] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def add_to_history(self, design: str):
        """Add a design version to history."""
        self.history.append(self.latest_design)
        self.latest_design = design
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert session to dictionary."""
        return {
            "id": self.session_id,
            "base_prompt": self.base_prompt,
            "latest_design": self.latest_design,
            "history": self.history,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class ContextManager:
    """Manages design session contexts (in-memory for now, Redis-ready for future)."""
    
    def __init__(self):
        self.sessions: Dict[str, SessionContext] = {}
    
    def create_session(
        self, 
        base_prompt: str, 
        initial_design: str,
        session_id: Optional[str] = None
    ) -> str:
        """
        Create a new design session.
        
        Args:
            base_prompt: The original user input/prompt
            initial_design: The initial design markdown
            session_id: Optional session ID (generated if not provided)
            
        Returns:
            Session ID
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        session = SessionContext(
            session_id=session_id,
            base_prompt=base_prompt,
            latest_design=initial_design
        )
        
        self.sessions[session_id] = session
        logger.info(f"📝 Created new session: {session_id}")
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionContext]:
        """Get a session by ID."""
        return self.sessions.get(session_id)
    
    def update_session(
        self, 
        session_id: str, 
        updated_design: str,
        add_to_history: bool = True
    ) -> bool:
        """
        Update a session with new design.
        
        Args:
            session_id: Session ID
            updated_design: Updated design markdown
            add_to_history: Whether to add current design to history
            
        Returns:
            True if updated, False if session not found
        """
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        if add_to_history:
            session.add_to_history(updated_design)
        else:
            session.latest_design = updated_design
            session.updated_at = datetime.now()
        
        logger.info(f"💾 Updated session: {session_id}")
        return True
    
    def get_or_create_session(
        self,
        base_prompt: str,
        design: str,
        session_id: Optional[str] = None
    ) -> str:
        """
        Get existing session or create new one.
        
        Args:
            base_prompt: Base prompt/instruction
            design: Current design markdown
            session_id: Optional session ID
            
        Returns:
            Session ID
        """
        if session_id and session_id in self.sessions:
            # Update existing session
            self.update_session(session_id, design, add_to_history=False)
            return session_id
        
        # Create new session
        return self.create_session(base_prompt, design, session_id)
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"🗑️  Deleted session: {session_id}")
            return True
        return False

