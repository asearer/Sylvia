
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

    # --- Command Callbacks ---
    def hello_callback():
        import random
        greetings = ["Hello there!", "Hi! I am online.", "Greetings, user.", "Hello! How can I help?"]
        return random.choice(greetings)

    def status_callback():
        # In a real system, checking other services via health pings
        return "All systems nominal. Agent Core, Voice Services, and Avatar Bridge are active."

    def time_callback():
        from datetime import datetime
        now = datetime.now().strftime("%I:%M %p")
        return f"It is currently {now}."

    def sing_callback():
        return "La la la! I am a digital entity, but I can still hold a tune. Do re mi fa so la ti do!"

    # --- Register Commands ---
    processor.register_command("hello", hello_callback)
    processor.register_command("hi", hello_callback)
    processor.register_command("status", status_callback)
    processor.register_command("time", time_callback)
    processor.register_command("sing", sing_callback)
    
    logger.info("Voice commands registered: hello, status, time, sing")
    
    def on_message(event_type, payload):
        if event_type == "user_input":
            logger.info(f"Processing user input: {payload}")
            
            # Simple keyword check / processing
            # Real implementation would use LLM router
            
            # Try to execute as command
            command_result = processor.process_command(payload)
            
            response_text = ""
            if command_result and command_result.get("executed"):
                response_text = command_result.get("response")
            else:
                # Fallback to chat / LLM
                # For now, just echo if not a command
                response_text = f"I heard you say: {payload}"
                
            logger.info(f"Agent Response: {response_text}")
            messenger.publish("agent_response", response_text)
            
    try:
        messenger.subscribe(on_message)
    except KeyboardInterrupt:
        logger.info("Stopping Agent Core...")
        messenger.close()

if __name__ == "__main__":
    main()
