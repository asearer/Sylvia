"""
Model Registry.

Auto-discovers GGUF models in the /models directory and tracks their metadata.
"""

import os
import logging
from typing import Dict, List, Optional, Any
from .models import ModelProfile, SafetyProfile, IntendedUse

logger = logging.getLogger("agent-core.llm.registry")

class ModelRegistry:
    def __init__(self, models_dir: str = "/models"):
        self.models_dir = models_dir
        self.available_models: Dict[str, ModelProfile] = {}
        
        # Configuration for known models
        self.model_configs = {
            "qwen2.5-3b-instruct-q4_k_m.gguf": {
                "display_name": "Qwen2.5-3B",
                "provider": "Qwen",
                "safety_profile": "uncensored",
                "intended_use": "testing",
                "description": "Uncensored model for safety testing."
            },
            "phi-3-mini-4k-instruct.gguf": {
                "display_name": "Phi-3-Mini",
                "provider": "Microsoft",
                "safety_profile": "uncensored",
                "intended_use": "testing",
                "description": "Lightweight model for rapid testing."
            },
            "llama-3.2-3b-instruct-q4_k_m.gguf": {
                "display_name": "LLaMA-3.2-3B",
                "provider": "Meta",
                "safety_profile": "guarded",
                "intended_use": "production",
                "description": "Production-grade guarded model."
            }
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
                
                # Get config or Use defaults for unknown models
                config = self.model_configs.get(filename, {
                    "display_name": filename.replace(".gguf", ""),
                    "provider": "Unknown",
                    "safety_profile": "minimally_guarded", # Default to minimal
                    "intended_use": "fallback",
                    "description": "Unknown local model."
                })
                
                # Estimate size
                size_mb = os.path.getsize(os.path.join(self.models_dir, filename)) / (1024 * 1024)
                
                profile = ModelProfile(
                    id=model_id,
                    display_name=config["display_name"],
                    provider=config["provider"],
                    size_mb=round(size_mb, 2),
                    inference_type="local",
                    safety_profile=config["safety_profile"],
                    intended_use=config["intended_use"],
                    description=config["description"]
                )
                
                self.available_models[profile.display_name] = profile
                logger.info(f"Discovered model: {profile.display_name} [{profile.safety_profile}]")

    def list_models(self) -> List[ModelProfile]:
        """Return list of available model profiles."""
        return list(self.available_models.values())

    def get_model_info(self, name: str) -> Optional[ModelProfile]:
        """Get metadata for a specific friendly name."""
        return self.available_models.get(name)
