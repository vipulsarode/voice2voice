import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    groq_api : str = os.getenv('GROQ_API_KEY')
    weatherstack_api : str = os.getenv('WEATHERSTACK_API')
    openai_api_key : str = os.getenv('OPENAI_API')


@lru_cache
def get_settings() -> Settings:
    return Settings()


#example run
settings = get_settings()
print(settings.groq_api)