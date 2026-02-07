
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
    
    def on_message(event_type, payload):
        if event_type == "user_input":
            logger.info(f"Processing user input: {payload}")
            
            # Simple keyword check / processing
            # Real implementation would use LLM router
            
            # Try to execute as command
            command_result = processor.process_command(payload)
            
            response_text = ""
            if command_result:
                response_text = f"Command executed: {command_result}"
                # For non-string returns, cast to str
                if not isinstance(command_result, str):
                   response_text = f"Command executed. Result: {command_result}" 
            else:
                # Fallback to chat
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
