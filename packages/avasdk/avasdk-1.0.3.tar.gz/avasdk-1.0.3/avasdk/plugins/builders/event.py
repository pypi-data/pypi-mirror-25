def build_event(raw):
    """
    """
    index = 0
    results = ' '.join(raw.split()).split(' ')
    event = {'action': None, 'target': None, 'args': None}
    for key, result in zip(event, results):
        event[key] = ' '.join(
            map(str, results[index:])) if key == 'args' else result
        index += 1
    return event
