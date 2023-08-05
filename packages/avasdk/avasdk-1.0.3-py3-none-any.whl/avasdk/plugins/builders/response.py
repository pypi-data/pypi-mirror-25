def build_response(author, result=None, display=None):
    """
    """
    response = {
        'type': 'response',
        'from': author,
        'tts': result if result else (author + ' just finished to proceed.'),
        'display': display
    }
    return response
