import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    SYMBOL: str = os.getenv('SYMBOL')
    EXCHANGE: str = os.getenv('EXCHANGE')

settings = Settings()