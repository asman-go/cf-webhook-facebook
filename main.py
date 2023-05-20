from src.config import Config


def verification_request(data, verification_token: str):

    if 'hub.challenge' in data and 'hub.mode' in data and 'hub.verify_token' in data:
        print(f'Receive Webhook Verification Request. hub.mode is {data["hub.mode"]}')

        if data['hub.verify_token'] == verification_token:
            print('hub.verify_token is correct')

            return data['hub.challenge']

    return ''


def event_handler(event, context):
    print(event)
    config = Config()
    if 'queryStringParameters' in event:
        queryStringParameters = event['queryStringParameters']
        challenge = verification_request(queryStringParameters, config.WEBHOOK_VERIFICATION_TOKEN)
        if challenge:
            print(f'Challenge {challenge}')
            return {
                'response': {
                    'statusCode': 200,
                    'body': challenge,
                    'text': 'test'
                }
            }

    return {
        'response': {
            'text': 'OK'
        }
    }