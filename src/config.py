import pydantic

class Config(pydantic.BaseSettings):
    WEBHOOK_VERIFICATION_TOKEN: str