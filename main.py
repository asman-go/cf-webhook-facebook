import hashlib
import hmac
import json

from src.config import Config


def x_hub_signature_verify(event, config: Config):
    if 'body' in event and 'headers' in event and 'X-Hub-Signature-256' in event['headers']:
        body = event['body']
        signature = event['headers']['X-Hub-Signature-256'].replace('sha256=', '')

        h = hmac.new( config.FACEBOOK_CLIENT_SECRET.encode(), body.encode(), hashlib.sha256 )
        digest = h.hexdigest()

        return digest == signature
    
    return False


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
    # Verification Request: https://developers.facebook.com/docs/graph-api/webhooks/getting-started
    if 'queryStringParameters' in event:
        queryStringParameters = event['queryStringParameters']
        challenge = verification_request(queryStringParameters, config.WEBHOOK_VERIFICATION_TOKEN)
        if challenge:
            # print(f'Challenge {challenge}')
            return {
                'statusCode': 200,
                'body': challenge
            }
    
    # certificate_transparency event: https://developers.facebook.com/docs/certificate-transparency/certificates-webhook#certificate-alert-webhook
    if (x_hub_signature_verify(event, config)):
        body = event['body']
        data = json.loads(body)
        FACEBOOK_EVENT = 'certificate_transparency'
        if 'object' in data and 'entry' in data and data['object'] == FACEBOOK_EVENT:
            for entry in data['entry']:
                print(f'New entry: {entry}')
                if 'changed_fields' in entry and 'certificate' in entry['changed_fields']:
                    print(f'I need to get information about certificate with id = {entry["id"]}')
                    # TODO
        
        return {
            'statusCode': 200,
        }
    
    return {
        'statusCode': 401,
    }