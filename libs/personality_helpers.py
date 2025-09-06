# libs/personality_helpers.py

def snapshot_active_profiles(persona):
    """
    Returns a copy of the current active profile weights.
    """
    return persona.active_profiles.copy()

def micro_personality_count(persona, threshold=0.05):
    """
    Counts micro-personalities with weight above the threshold.
    """
    return sum(1 for mp in persona.micro_personalities.values() if mp["weight"] > threshold)

def update_session_history(persona, session_state):
    """
    Updates session state dictionaries for weights, micro-personality count, and interactions.
    `session_state` should be a dict with keys:
      - 'weights_history'
      - 'micro_count_history'
      - 'interactions_history'
    """
    snapshot = snapshot_active_profiles(persona)
    session_state['weights_history'].append(snapshot)
    session_state['micro_count_history'].append(micro_personality_count(persona))
    session_state['interactions_history'].append(persona.interactions)
