import json
import typing

from src.config import Config
from src.utils.hmac_sha256 import hmac_digest
from src.utils.pem import get_domains_from_certificate


def x_hub_signature_verify(event, config: Config):
    if 'body' in event and 'headers' in event and 'X-Hub-Signature-256' in event['headers']:
        body = event['body']
        signature = event['headers']['X-Hub-Signature-256'].replace('sha256=', '')
        digest = hmac_digest(config.FACEBOOK_CLIENT_SECRET, body)

        return digest == signature
    
    return False


def handler(event, config: Config) -> typing.Dict[str, typing.List[str]]:
    domains_dict = {}
    # certificate_transparency event: https://developers.facebook.com/docs/certificate-transparency/certificates-webhook#certificate-alert-webhook
    if (x_hub_signature_verify(event, config)):
        body = event['body']
        data = json.loads(body)
        FACEBOOK_EVENT = 'certificate_transparency'
        if 'object' in data and 'entry' in data and data['object'] == FACEBOOK_EVENT:
            for entry in data['entry']:
                if 'changed_fields' in entry and 'certificate' in entry['changed_fields']:
                    # I don't know how to do that
                    print(f'I need to get information about certificate with id = {entry["id"]}, entry = {entry}')

                if 'changes' in entry:
                    # Parse certificate and get domains from that
                    for change in entry['changes']:
                        parent_domain, domains = get_domains_from_certificate(
                            change['value']['certificate_pem']
                        )
                        if parent_domain not in domains_dict:
                            domains_dict[parent_domain] = []
                        domains_dict[parent_domain].extend(domains)
    
    return domains_dict
