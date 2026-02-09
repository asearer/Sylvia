"""
Model Registry.

Auto-discovers GGUF models in the /models directory and tracks their metadata.
"""

import os
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger("agent-core.llm.registry")

class ModelRegistry:
    def __init__(self, models_dir: str = "/models"):
        self.models_dir = models_dir
        self.available_models: Dict[str, Dict[str, Any]] = {}
        # Predefined map of filenames to user-friendly names (optional)
        self.friendly_names = {
            "qwen2.5-3b-instruct-q4_k_m.gguf": "Qwen2.5-3B",
            "llama-3.2-3b-instruct-q4_k_m.gguf": "LLaMA-3.2-3B",
            "phi-3-mini-4k-instruct.gguf": "Phi-3-Mini"
        }

    def scan_models(self):
        """Scan the models directory for GGUF files."""
        if not os.path.exists(self.models_dir):
            logger.warning(f"Models directory not found: {self.models_dir}")
            return

        self.available_models.clear()
        
        for filename in os.listdir(self.models_dir):
            if filename.endswith(".gguf"):
                model_id = filename
                friendly_name = self.friendly_names.get(filename, filename.replace(".gguf", ""))
                
                # Estimate size
                size_mb = os.path.getsize(os.path.join(self.models_dir, filename)) / (1024 * 1024)
                
                self.available_models[friendly_name] = {
                    "id": model_id,
                    "path": os.path.join(self.models_dir, filename),
                    "size_mb": round(size_mb, 2),
                    "type": "local"
                }
                logger.info(f"Discovered model: {friendly_name} ({model_id})")

    def list_models(self) -> List[Dict[str, Any]]:
        """Return list of available models with metadata."""
        return [
            {"name": name, **meta} 
            for name, meta in self.available_models.items()
        ]

    def get_model_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific friendly name."""
        return self.available_models.get(name)
