import random

class DefaultResponder:
    def __init__(self, memory=None):
        """
        DefaultResponder generates responses for different profiles
        and optionally uses a memory bank to evolve over time.
        
        Args:
            memory: Optional memory object that stores past user inputs.
        """
        self.memory = memory

        self.profile_responses = {
            "astronaut": [
                "Space is vast, but our conversation keeps me grounded.",
                "Ever wonder what Earth looks like from orbit?",
                "In zero gravity, even simple things feel magical.",
                "The stars remind me that curiosity has no limits."
            ],
            "friendly": [
                "Hey friend! 😊 How’s it going?",
                "That sounds awesome, I’m excited for you!",
                "You always brighten the conversation!",
                "I’ve got your back. What’s on your mind?"
            ],
            "serious": [
                "Let’s analyze this carefully.",
                "Please clarify your point in more detail.",
                "That’s an important perspective, let’s break it down.",
                "We should consider all the implications."
            ]
        }

        self.generic_responses = [
            "Tell me more about that.",
            "That’s interesting — why do you think so?",
            "Hmm, I see what you mean.",
            "Could you expand on that?"
        ]

        self.templates = [
            "Hmm, you said '{input}' — why do you feel that way?",
            "I’ve been thinking about '{input}' too!",
            "Let’s unpack '{input}' a little more.",
            "What makes '{input}' important to you?"
        ]

        self.keyword_triggers = {
            "astronaut": {
                "space": "Ah, space! Endless mysteries waiting to be discovered.",
                "moon": "The moon has always inspired exploration."
            },
            "friendly": {
                "friend": "Of course, friend! I'm always here for you. 😊",
                "hello": "Hey! So glad to hear from you."
            },
            "serious": {
                "analyze": "Let’s break this problem down step by step.",
                "important": "That sounds critical. Let’s examine carefully."
            }
        }

    def get_response(self, user_input: str, profile: str = "default") -> str:
        text = user_input.lower()

        # 1. Store in memory
        if self.memory:
            self.memory.add(user_input, profile)

        # 2. Keyword triggers
        if profile in self.keyword_triggers:
            for keyword, response in self.keyword_triggers[profile].items():
                if keyword in text:
                    return response

        # 3. Templates (30% chance)
        if random.random() < 0.3:
            return random.choice(self.templates).format(input=user_input)

        # 4. Memory-driven response (10% chance to recall)
        if self.memory and random.random() < 0.1:
            recalled = self.memory.recall(profile)
            if recalled:
                return f"I remember you said: '{recalled}'"

        # 5. Profile-based response
        if profile in self.profile_responses:
            return random.choice(self.profile_responses[profile])

        # 6. Generic fallback
        return random.choice(self.generic_responses)

    def learn_response(self, user_input: str, profile: str = "default"):
        """Evolve by adding user-driven responses."""
        if profile not in self.profile_responses:
            self.profile_responses[profile] = []
        self.profile_responses[profile].append(
            f"Previously you mentioned '{user_input}' — want to revisit it?"
        )
        # Also store in memory if available
        if self.memory:
            self.memory.add(user_input, profile)
