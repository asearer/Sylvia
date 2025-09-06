def normalize(data):
    return [(x - min(data)) / (max(data) - min(data)) for x in data]
