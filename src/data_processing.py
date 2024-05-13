# src/data_processing.py

def preprocess_data(data):
    processed_data = []
    for conversation in data:
        # Placeholder preprocessing steps
        processed_conversation = []
        for message in conversation:
            # Tokenization, lowercasing, etc.
            processed_message = message.lower().split()
            processed_conversation.append(processed_message)
        processed_data.append(processed_conversation)
    return processed_data

