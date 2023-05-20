DOMAINS_TABLE_NAME = 'domains'
DOMAINS_TABLE_KEY_SCHEMA = [
    {
        'AttributeName': 'domain',
        'KeyType': 'HASH'
    }
]
DOMAINS_TABLE_ATTRIBUTE_DEFINITIONS = [
    {
        'AttributeName': 'domain',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'parent_domain',
        'AttributeType': 'S'
    }
]