"""
Console-based chat interface for AI personality experiments.
Uses personality and PersonalityVisualizer modules.
"""

from ai_personality.personality import Personality
from ai_personality.visualizer import PersonalityVisualizer

# Initialize AI personality
persona = Personality("astronaut", evolving=True)
visualizer = PersonalityVisualizer(persona)

print("Commands: /switch [name], /hybrid [name:weight,...], quit")
print("Bot evolves dynamically and creates emergent micro-personalities and idioms.")
print("Visualization of personality state will update after each message.")

while True:
    user_input = input("You: ")

    if user_input.lower().startswith("/switch"):
        parts = user_input.split()
        if len(parts) > 1:
            try:
                persona.switch_personality(parts[1])
                print(f"Switched to {parts[1]}")
            except ValueError as e:
                print(e)
        visualizer.show()
        continue

    if user_input.lower().startswith("/hybrid"):
        parts = user_input.split()
        if len(parts) > 1:
            weights = {}
            for pair in parts[1].split(","):
                try:
                    name, w = pair.split(":")
                    weights[name] = float(w)
                except:
                    print(f"Invalid format: {pair}. Use Name:Weight")
            try:
                persona.set_weighted_hybrid(weights)
                print(f"Weighted hybrid active: {', '.join([f'{k}({v})' for k,v in weights.items()])}")
            except ValueError as e:
                print(e)
        visualizer.show()
        continue

    if user_input.lower() in ["quit", "exit"]:
        break

    response = persona.chat(user_input)
    print(f"{', '.join(persona.active_profiles)} AI:", response)

    fb = input("Feedback (+/-/enter to skip): ")
    feedback = 1 if fb == "+" else -1 if fb == "-" else None
    if feedback:
        persona._automatic_evolution(user_input, response, feedback)
        persona.save()

    # Update visualization
    visualizer.show()
