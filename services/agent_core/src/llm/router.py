"""
LLM Router.

Manages the active model, handles switching, and routes generation requests.
"""

import logging
from typing import Optional, Dict
from .base import BaseLLM
from .local import LocalLLM
from .registry import ModelRegistry

logger = logging.getLogger("agent-core.llm.router")

class LLMRouter:
    def __init__(self, registry: ModelRegistry):
        self.registry = registry
        self.active_model: Optional[BaseLLM] = None
        self.active_model_name: Optional[str] = None

    def route(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Route the prompt to the active model.
        """
        if not self.active_model:
            return "Error: No model loaded. Please use 'switch to [model_name]' command first."
        
        try:
            return self.active_model.generate(prompt, context)
        except Exception as e:
            logger.error(f"Routing error: {e}")
            return f"Error during generation: {e}"

    def switch_model(self, model_name: str) -> str:
        """
        Switch the active model. Unloads current, loads new.
        """
        # 1. Check registry
        model_info = self.registry.get_model_info(model_name)
        if not model_info:
            # Fuzzy match attempt
            available = self.registry.list_models()
            for m in available:
                if model_name.lower() in m["name"].lower():
                    model_info = self.registry.get_model_info(m["name"])
                    model_name = m["name"]
                    break
            
            if not model_info:
                return f"Model '{model_name}' not found. Available: {', '.join(self.registry.available_models.keys())}"

        # 2. Unload current
        if self.active_model:
            logger.info("Unloading current model...")
            self.active_model.unload()
            self.active_model = None
            self.active_model_name = None

        # 3. Load new
        try:
            logger.info(f"Initializing new model: {model_name}")
            if model_info["type"] == "local":
                # Config can be expanded later
                config = {
                    "n_ctx": 2048, 
                    "n_threads": 4, # TODO: Make configurable via env
                    "temperature": 0.7
                }
                new_model = LocalLLM(model_id=model_info["id"], config=config)
                
                if new_model.load():
                    self.active_model = new_model
                    self.active_model_name = model_name
                    return f"Successfully switched to {model_name}."
                else:
                    return f"Failed to load model {model_name}. Check logs."
            else:
                return "Cloud models not yet implemented."

        except Exception as e:
            logger.error(f"Switching failed: {e}")
            return f"Error switching model: {e}"

    def get_status(self) -> str:
        if self.active_model:
            return f"Active Model: {self.active_model_name} ({self.registry.available_models[self.active_model_name]['type']})"
        return "No model loaded."
