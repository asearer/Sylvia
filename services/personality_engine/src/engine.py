
"""
Personality Engine Entrypoint.

This module serves as the main entry point for the Personality Engine service.
It coordinates the interaction between the user (via console or API) and the
underlying Personality model.

It supports pluggable LLM backends via the `LLMProvider` interface.
Can be run as CLI or (optionally) launch GUI.
"""

import argparse
import logging
from services.personality_engine.src.console_chat import main as console_main
from services.personality_engine.src.ai_personality.personality import Personality
from services.personality_engine.src.llm_provider import LLMProvider
# from src.gui import main as gui_main  # Uncomment when GUI is implemented

logger = logging.getLogger(__name__)

class MockLLM(LLMProvider):
    """
    Mock implementation of LLMProvider.
    """
    @property
    def name(self) -> str:
        return "MockLLM"

    def generate_response(self, prompt: str, context: list = None) -> str:
        logger.info(f"MockLLM generating response for: {prompt}")
        return f"I heard you say: {prompt}"

# Global personality instance for the engine
_engine_persona = Personality("Sylvia", evolving=True)

# Default provider
_llm_provider: LLMProvider = MockLLM()

def set_llm_provider(provider: LLMProvider):
    """
    Set the active LLM provider.
    """
    global _llm_provider
    _llm_provider = provider
    logger.info(f"LLM provider set to {provider.name}")

def process_message(message: str) -> str:
    """
    Process a message using the active LLM provider.
    
    Args:
        message (str): User message.
        
    Returns:
        str: Generated response.
    """
    # In a real scenario, we would retrieve context/history here
    return _llm_provider.generate_response(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Personality Engine")
    parser.add_argument("--mode", choices=["cli", "gui"], default="cli")
    args = parser.parse_args()

    if args.mode == "cli":
        console_main()
    elif args.mode == "gui":
        # gui_main()
        print("GUI not implemented yet")
