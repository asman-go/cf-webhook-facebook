import pydantic

class Config(pydantic.BaseSettings):
    WEBHOOK_VERIFICATION_TOKEN: str
    FACEBOOK_CLIENT_SECRET: str
     # YDB: via cli — ydb config profile get db1
    DOCUMENT_API_ENDPOINT: str = "https://example.com/path/to/your/db"
    REGION_NAME: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = "<key-id>"
    AWS_SECRET_ACCESS_KEY: str = "<secret-access-key>"