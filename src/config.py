""""env config file"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """env variables"""
    loki_instance_uri: str

config = Settings()
