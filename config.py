import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"環境変数 {name} が設定されていません")
    return value

SEARCH_KEYWORDS = get_env_var("SEARCH_KEYWORDS")
SEARCH_CATEGORY = get_env_var("SEARCH_CATEGORY")
SLACK_WEBHOOK_URL = get_env_var("SLACK_WEBHOOK_URL")
