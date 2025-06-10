"""
Chain Brain Service - Background service for continuous chain data feeding
"""

import logging
import threading
import time
import asyncio
from typing import Optional

from src.services.ai.chain_brain_orchestrator import get_chain_brain_orchestrator

logger = logging.getLogger(__name__)

class ChainBrainService:
    """Background service that continuously feeds blockchain data to o3-mini"""
    
    def __init__(self):
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.chain_brain = get_chain_brain_orchestrator()
        
    def start(self):
        """Start the chain brain feeding service"""
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._run_chain_brain, daemon=True)
        self.thread.start()
        logger.info("Chain Brain Service started - feeding live blockchain data to o3-mini")
        
    def stop(self):
        """Stop the chain brain feeding service"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Chain Brain Service stopped")
        
    def _run_chain_brain(self):
        """Run the chain brain feeding in background thread"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self.chain_brain.start_chain_brain_feeding())
        except Exception as e:
            logger.error(f"Chain brain feeding error: {e}")
        finally:
            loop.close()
            
    def get_status(self):
        """Get service status"""
        return {
            "running": self.is_running,
            "recent_insights": self.chain_brain.get_recent_insights(3) if self.is_running else []
        }

# Global service instance
_chain_brain_service = None

def get_chain_brain_service() -> ChainBrainService:
    """Get the global chain brain service"""
    global _chain_brain_service
    if _chain_brain_service is None:
        _chain_brain_service = ChainBrainService()
    return _chain_brain_service

def start_chain_brain_service():
    """Start the chain brain service"""
    service = get_chain_brain_service()
    service.start()

def stop_chain_brain_service():
    """Stop the chain brain service"""
    global _chain_brain_service
    if _chain_brain_service:
        _chain_brain_service.stop()