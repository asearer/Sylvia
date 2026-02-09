"""
Model Definitions and Profiles.

Defines the metadata structure for LLM models, including safety profiles.
"""

from dataclasses import dataclass, field
from typing import Literal, Optional

SafetyProfile = Literal["uncensored", "minimally_guarded", "guarded"]
IntendedUse = Literal["testing", "production", "fallback"]

@dataclass
class ModelProfile:
    id: str
    display_name: str
    provider: str
    size_mb: float
    inference_type: Literal["local", "cloud"]
    safety_profile: SafetyProfile
    intended_use: IntendedUse
    description: str = ""
    # Optional config overrides specific to this model
    default_config: dict = field(default_factory=dict)
