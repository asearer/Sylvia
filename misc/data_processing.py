# src/data_processing.py

def preprocess_data(data):
    """
    Preprocesses the given data, which is assumed to be a list of conversations, 
    where each conversation is a list of messages.

    Args:
    data (list): List of conversations, where each conversation is a list of messages.

    Returns:
    list: Processed data with conversations and messages tokenized and lowercased.
    """
    processed_data = []
    if not isinstance(data, list):
        raise TypeError("Input data must be a list of conversations.")
    
    for conversation in data:
        if not isinstance(conversation, list):
            raise TypeError("Each conversation in the input data must be a list of messages.")
        
        processed_conversation = []
        for message in conversation:
            if not isinstance(message, str):
                raise TypeError("Each message in the conversation must be a string.")
            
            processed_message = message.lower().split()
            processed_conversation.append(processed_message)
        processed_data.append(processed_conversation)
    return processed_data
