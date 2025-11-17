"""
console_chat.py

Console-based chat interface for AI personality experiments.

Features:
- Interactive chat with AI personality (dynamic evolution enabled)
- Personality switching and weighted hybrid modes
- Real-time feedback handling
- Visualization updates via PersonalityVisualizer
- Simple input validation and error handling

Dependencies:
- ai_personality.personality.Personality
- ai_personality.visualizer.PersonalityVisualizer
"""

from ai_personality.personality import Personality
from ai_personality.visualizer import PersonalityVisualizer

def main():
    """Main loop for the console chat interface."""
    # Initialize AI personality and visualizer
    persona = Personality("astronaut", evolving=True)
    visualizer = PersonalityVisualizer(persona)

    print("Commands: /switch [name], /hybrid [name:weight,...], quit")
    print("Bot evolves dynamically and creates emergent micro-personalities and idioms.")
    print("Visualization of personality state updates after each message.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # Handle exit
        if user_input.lower() in ["quit", "exit"]:
            print("Exiting...")
            break

        # Handle commands
        if user_input.startswith("/switch"):
            handle_switch(user_input, persona, visualizer)
            continue

        if user_input.startswith("/hybrid"):
            handle_hybrid(user_input, persona, visualizer)
            continue

        # Normal message
        response = persona.chat(user_input)
        print(f"{', '.join(persona.active_profiles)} AI: {response}")

        # Feedback
        handle_feedback(user_input, response, persona)

        # Update visualization
        visualizer.show()


def handle_switch(command, persona, visualizer):
    """
    Handle '/switch' command to change active personality.

    Args:
        command (str): Raw command string.
        persona (Personality): AI personality instance.
        visualizer (PersonalityVisualizer): Visualization instance.
    """
    parts = command.split()
    if len(parts) < 2:
        print("Usage: /switch [profile_name]")
        return
    try:
        persona.switch_personality(parts[1])
        print(f"Switched to {parts[1]}")
    except ValueError as e:
        print(f"Error: {e}")
    visualizer.show()


def handle_hybrid(command, persona, visualizer):
    """
    Handle '/hybrid' command to set weighted hybrid profiles.

    Args:
        command (str): Raw command string.
        persona (Personality): AI personality instance.
        visualizer (PersonalityVisualizer): Visualization instance.
    """
    parts = command.split()
    if len(parts) < 2:
        print("Usage: /hybrid [profile:weight,...]")
        return

    weights = {}
    invalid_entries = []

    for pair in parts[1].split(","):
        try:
            name, w = pair.split(":")
            weights[name] = float(w)
        except ValueError:
            invalid_entries.append(pair)

    if invalid_entries:
        print(f"Invalid format: {', '.join(invalid_entries)}. Use Name:Weight")
        return

    try:
        persona.set_weighted_hybrid(weights)
        print(f"Weighted hybrid active: {', '.join([f'{k}({v})' for k,v in weights.items()])}")
    except ValueError as e:
        print(f"Error: {e}")

    visualizer.show()


def handle_feedback(user_input, bot_response, persona):
    """
    Prompt user for feedback on bot response and apply evolution if given.

    Args:
        user_input (str): Original user input.
        bot_response (str): Bot's response.
        persona (Personality): AI personality instance.
    """
    fb = input("Feedback (+/-/enter to skip): ").strip()
    feedback = None
    if fb == "+":
        feedback = 1
    elif fb == "-":
        feedback = -1

    if feedback is not None:
        persona._automatic_evolution(user_input, bot_response, feedback)
        persona.save()
        print("Feedback recorded ✅")


if __name__ == "__main__":
    main()
