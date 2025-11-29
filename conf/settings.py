import ast
import os

from dotenv import load_dotenv
from infisical_sdk import InfisicalSDKClient

load_dotenv()


# Инициализация клиента
client = InfisicalSDKClient(
    host=os.getenv('INFISICAL_HOST'),
    token=os.getenv('INFISICAL_TOKEN'),
    cache_ttl=300
)


def load_project_secrets(project_slug: str):
    resp = client.secrets.list_secrets(
        project_slug=project_slug,
        environment_slug=os.getenv('ENVIRONMENT_SLUG'),
        secret_path="/"
    )
    return {s['secretKey']: s['secretValue'] for s in resp.to_dict()['secrets']}

# Загружаем общие секреты
shared_secrets = load_project_secrets("shared-all")

# Загружаем проектные секреты
project_secrets = load_project_secrets("signals-btc")

# Объединяем: проектные перезаписывают общие при совпадении ключей
all_secrets = {**shared_secrets, **project_secrets}

# Добавляем в окружение
os.environ.update(all_secrets)

class Settings:
    SYMBOL: str = os.getenv('SYMBOL')
    EXCHANGE: str = os.getenv('EXCHANGE')

    PRINT_DEBUG: bool = ast.literal_eval(os.getenv('PRINT_DEBUG'))

    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT'))
    REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD')

settings = Settings()