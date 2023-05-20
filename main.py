import hashlib
import hmac

from src.config import Config


def x_hub_signature_verify(payload: str, signature: str, config: Config):
    h = hmac.new( config.FACEBOOK_CLIENT_SECRET.encode(), payload.encode(), hashlib.sha256 )
    digest = h.hexdigest()
    print(digest)
    print(signature)


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
                'statusCode': 200,
                'body': challenge
            }
        
    if 'body' in event and 'headers' in event and 'X-Hub-Signature-256' in event['headers']:
        body = event['body']
        signature = event['headers']['X-Hub-Signature-256']
        x_hub_signature_verify(body, signature, config)
        

    return {
        'statusCode': 401,
    }