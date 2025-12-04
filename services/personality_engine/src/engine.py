
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

import google.generativeai as genai
import openai
import anthropic
import time
from datetime import datetime

# --- Analytics ---
class AnalyticsTracker:
    def __init__(self):
        self.logs = []

    def log_interaction(self, service: str, model: str, input_text: str, output_text: str, latency: float):
        # Estimate tokens (rough approximation: 4 chars per token)
        input_tokens = len(input_text) // 4
        output_tokens = len(output_text) // 4
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency": latency
        }
        self.logs.append(entry)
        # Keep only last 1000 logs to avoid memory issues in this demo
        if len(self.logs) > 1000:
            self.logs.pop(0)

    def get_stats(self):
        return self.logs

_analytics = AnalyticsTracker()

def get_analytics_data():
    return _analytics.get_stats()

# --- Providers ---

class GeminiLLM(LLMProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "Gemini Pro"

    def generate_response(self, prompt: str, context: list = None) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini Error: {e}")
            return f"Error from Gemini: {e}"

class OpenAILLM(LLMProvider):
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "GPT-3.5 Turbo"

    def generate_response(self, prompt: str, context: list = None) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI Error: {e}")
            return f"Error from OpenAI: {e}"

class AnthropicLLM(LLMProvider):
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "Claude 3 Sonnet"

    def generate_response(self, prompt: str, context: list = None) -> str:
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic Error: {e}")
            return f"Error from Anthropic: {e}"

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

def set_llm_provider(provider_type: str, api_key: str = None):
    """
    Set the active LLM provider.
    """
    global _llm_provider
    
    if provider_type == "Gemini":
        _llm_provider = GeminiLLM(api_key)
    elif provider_type == "OpenAI":
        _llm_provider = OpenAILLM(api_key)
    elif provider_type == "Anthropic":
        _llm_provider = AnthropicLLM(api_key)
    else:
        # Fallback to local
        if not isinstance(_llm_provider, HuggingFaceLLM):
            _llm_provider = HuggingFaceLLM()
            
    logger.info(f"LLM provider set to {_llm_provider.name}")

def process_message(message: str, service_name: str = "chat") -> str:
    """
    Process a message using the active LLM provider.
    
    Args:
        message (str): User message.
        service_name (str): Name of the service calling this (for analytics).
    """
    start_time = time.time()
    response = _llm_provider.generate_response(message)
    end_time = time.time()
    latency = end_time - start_time
    
    # Log analytics
    _analytics.log_interaction(service_name, _llm_provider.name, message, response, latency)
    
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Personality Engine")
    parser.add_argument("--mode", choices=["cli", "gui"], default="cli")
    args = parser.parse_args()

    if args.mode == "cli":
        console_main()
    elif args.mode == "gui":
        # gui_main()
        print("GUI not implemented yet")
