
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

from transformers import pipeline
import torch

class HuggingFaceLLM(LLMProvider):
    """
    Real implementation using Hugging Face 'distilgpt2' for chat.
    """
    def __init__(self):
        self.pipeline = None
        self.device = -1
        self._load_model()

    def _load_model(self):
        try:
            if torch.cuda.is_available():
                self.device = 0
                logger.info("Chat: CUDA GPU detected. Using GPU.")
            elif torch.backends.mps.is_available():
                self.device = "mps"
                logger.info("Chat: Apple MPS detected. Using GPU.")
            else:
                self.device = -1
                logger.info("Chat: No GPU detected. Using CPU.")

            self.pipeline = pipeline(
                "text-generation", 
                model="distilgpt2", 
                device=self.device,
                max_new_tokens=100,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                repetition_penalty=1.2,
                pad_token_id=50256  # EOS token for GPT-2
            )
        except Exception as e:
            logger.error(f"Chat: Failed to load model. Error: {e}")

    @property
    def name(self) -> str:
        return "HuggingFaceLLM (distilgpt2)"

    def generate_response(self, prompt: str, context: list = None) -> str:
        if self.pipeline:
            try:
                # Simple generation
                response = self.pipeline(prompt, num_return_sequences=1)[0]['generated_text']
                # Basic cleanup: remove the prompt from the response if it's included
                if response.startswith(prompt):
                    response = response[len(prompt):].strip()
                return response
            except Exception as e:
                logger.error(f"Chat Error: {e}")
                return f"Error generating response: {e}"
        else:
            return "Chat Model not loaded."

# Global personality instance for the engine
_engine_persona = Personality("Sylvia", evolving=True)

# Default provider
_llm_provider: LLMProvider = HuggingFaceLLM()

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
