"""
Local LLM Adapter using llama-cpp-python.

Handles loading GGUF models for CPU inference.
"""

import os
import logging
from typing import Optional, Dict

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

from .base import BaseLLM

logger = logging.getLogger("agent-core.llm.local")

class LocalLLM(BaseLLM):
    def __init__(self, model_id: str, config: Optional[Dict] = None):
        super().__init__(model_id, config)
        self._llm = None
        # Default config optimized for CPU (as per user constraints)
        self.context_window = self.config.get("n_ctx", 2048)
        self.n_threads = self.config.get("n_threads", 4) # Adjust based on CPU cores
        self.model_path = os.path.join("/models", model_id)

    def load(self) -> bool:
        if self._llm:
            return True

        if not os.path.exists(self.model_path):
            logger.error(f"Model file not found: {self.model_path}")
            return False

        if Llama is None:
            logger.error("llama-cpp-python not installed.")
            return False

        try:
            logger.info(f"Loading local model: {self.model_id} (CPU, threads={self.n_threads})")
            self._llm = Llama(
                model_path=self.model_path,
                n_ctx=self.context_window,
                n_threads=self.n_threads,
                verbose=False
            )
            return True
        except Exception as e:
            logger.error(f"Failed to load model {self.model_id}: {e}")
            return False

    def unload(self) -> bool:
        if self._llm:
            logger.info(f"Unloading model: {self.model_id}")
            del self._llm
            self._llm = None
            import gc
            gc.collect()
        return True

    def is_loaded(self) -> bool:
        return self._llm is not None

    def generate(self, prompt: str, context: Optional[Dict] = None) -> str:
        if not self._llm:
            raise RuntimeError("Model not loaded. Call load() first.")

        # Prepare generation parameters
        max_tokens = self.config.get("max_tokens", 512)
        temp = self.config.get("temperature", 0.7)
        top_p = self.config.get("top_p", 0.9)
        stop = self.config.get("stop", ["User:", "\n\n"])

        try:
            # Simple instruct formatting (could be improved per model)
            # For now, we assume the prompt is pre-formatted or raw
            output = self._llm(
                prompt,
                max_tokens=max_tokens,
                temperature=temp,
                top_p=top_p,
                stop=stop,
                echo=False
            )
            return output["choices"][0]["text"].strip()
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return f"Error generating response: {e}"
