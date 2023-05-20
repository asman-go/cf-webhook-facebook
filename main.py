def event_handler(event, context):
    print(event)
    return {
        'response': {
            'text': 'OK'
        }
    }