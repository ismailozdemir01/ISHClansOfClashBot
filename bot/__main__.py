from bot.app import create_app
from bot.core.config import get_settings
import uvicorn

if __name__ == "__main__":
    s = get_settings()
    uvicorn.run(create_app(), host=s.host, port=s.port)
