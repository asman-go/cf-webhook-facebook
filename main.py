
from src.config import Config

from src.handlers.verification_handler import handler as verification_request_handler
from src.handlers.ctlog_event_handler import handler as certificate_transparency_event_handler
from src.database import DocumentAPI


def event_handler(event, context):
    # print(event)
    config = Config()

    response = verification_request_handler(event, config)
    if response:
        return response
    
    domains_dict = certificate_transparency_event_handler(event, config)
    dynamodb = DocumentAPI(config)
    for parent_domain in domains_dict:
        dynamodb.upsert_domains(parent_domain, list(set(domains_dict[parent_domain])))

    return {
        'statusCode': 200,
    }