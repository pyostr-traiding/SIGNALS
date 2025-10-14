import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    SYMBOL: str = os.getenv('SYMBOL')
    EXCHANGE: str = os.getenv('EXCHANGE')

    PRINT_DEBUG: bool = False

settings = Settings()