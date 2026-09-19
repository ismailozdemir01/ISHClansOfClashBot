import uvicorn
from bot.app import create_app
from bot.core.config import get_settings

if __name__=="__main__":
    settings=get_settings()
    uvicorn.run(create_app(),host=settings.host,port=settings.port)
