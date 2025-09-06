# src/interface/cli.py

from ai_personality.personality import Personality
from libs.personality_helpers import snapshot_active_profiles, micro_personality_count, update_session_history

def start_cli():
    bot_persona = Personality("astronaut", evolving=True)
    session_state = {'weights_history': [], 'micro_count_history': [], 'interactions_history': []}

    print("Start chatting with Sylvia! Commands: /switch [profile], /hybrid [profile:weight,...], exit")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        response = handle_input(bot_persona, user_input, session_state)
        print(f"Sylvia: {response}")

def handle_input(persona, msg, session_state):
    msg_lower = msg.lower()
    if msg_lower.startswith("/switch"):
        parts = msg.split()
        if len(parts) > 1:
            persona.switch_personality(parts[1])
            update_session_history(persona, session_state)
            return f"Switched to {parts[1]}"

    if msg_lower.startswith("/hybrid"):
        parts = msg.split()
        if len(parts) > 1:
            weights = {}
            for pair in parts[1].split(","):
                try:
                    name, w = pair.split(":")
                    weights[name] = float(w)
                except:
                    return f"Invalid format: {pair}. Use Name:Weight"
            persona.set_weighted_hybrid(weights)
            update_session_history(persona, session_state)
            return f"Weighted hybrid applied: {weights}"

    # Normal chat
    response = persona.chat(msg)
    update_session_history(persona, session_state)
    return response

