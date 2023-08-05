def build_request(author, payload=None, display=None):
    """
    """
    request = {
        'type':
        'request',
        'from':
        author,
        'tts':
        payload if payload else
        (author + ' is waiting for your answer in order to proceed.'),
        'display':
        display
    }
    return request
