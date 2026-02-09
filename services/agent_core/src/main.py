
import logging
import sys
import time
from pathlib import Path

# Ensure libs approachability
sys.path.append("/app")

from libs.ipc.messenger import Messenger
# Corrected import after directory rename
from services.agent_core.planning.command_processor import CommandProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent-core")

def main():
    logger.info("Starting Agent Core Service...")
    
    messenger = Messenger(channel="sylvia:events")
    processor = CommandProcessor()
    
    # --- LLM Setup ---
    from services.agent_core.src.llm.registry import ModelRegistry
    from services.agent_core.src.llm.router import LLMRouter

    registry = ModelRegistry()  # Defaults to /models
    registry.scan_models()
    llm_router = LLMRouter(registry)

    # --- Command Callbacks ---
    def hello_callback():
        import random
        greetings = ["Hello there!", "Hi! I am online.", "Greetings, user.", "Hello! How can I help?"]
        return random.choice(greetings)

    def status_callback():
        llm_status = llm_router.get_status()
        return f"All systems nominal. {llm_status}"

    def time_callback():
        from datetime import datetime
        now = datetime.now().strftime("%I:%M %p")
        return f"It is currently {now}."

    def sing_callback():
        return "La la la! I am a digital entity, but I can still hold a tune. Do re mi fa so la ti do!"

    def list_models_callback():
        models = registry.list_models()
        if not models:
            return "No local models found in /models directory."
        
        response = "Available models:\n"
        for m in models:
            response += f"- {m.display_name} [{m.safety_profile}]\n"
        return response.strip()

    def switch_model_callback(target_model: str):
        pass
        
    def current_model_callback():
        status = llm_router.get_status()
        safe_mode = "ON" if llm_router.safe_mode else "OFF"
        return f"{status} | Safe Mode: {safe_mode}"

    # --- Register Commands ---
    processor.register_command("hello", hello_callback)
    processor.register_command("hi", hello_callback)
    processor.register_command("status", status_callback)
    processor.register_command("time", time_callback)
    processor.register_command("sing", sing_callback)
    processor.register_command("list models", list_models_callback)
    processor.register_command("current model", current_model_callback)
    
    logger.info("Voice commands registered: hello, status, time, sing, list models, current model")
    
    def on_message(event_type, payload):
        if event_type == "user_input":
            logger.info(f"Processing user input: {payload}")
            
            # Special handling for "Switch to X" since our simple processor doesn't parse args well yet
            if payload.lower().startswith("switch to"):
                target = payload[9:].strip() # len("switch to") + 1
                result = llm_router.switch_model(target)
                response_text = result
                logger.info(f"Agent Response: {response_text}")
                messenger.publish("agent_response", response_text)
                return

            # Try to execute as command
            command_result = processor.process_command(payload)
            
            response_text = ""
            if command_result and command_result.get("executed"):
                response_text = command_result.get("response")
            else:
                # LLM Generation
                if llm_router.active_model:
                     logger.info("Routing to LLM...")
                     response_text = llm_router.route(payload)
                else:
                    # Fallback if no LLM loaded
                    response_text = f"I heard you say: {payload}. (No LLM loaded. Say 'List models' to see options)"
                
            logger.info(f"Agent Response: {response_text}")
            messenger.publish("agent_response", response_text)
            
    try:
        messenger.subscribe(on_message)
    except KeyboardInterrupt:
        logger.info("Stopping Agent Core...")
        if llm_router.active_model:
            llm_router.active_model.unload()
        messenger.close()

if __name__ == "__main__":
    main()
