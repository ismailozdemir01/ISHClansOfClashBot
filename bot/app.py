from contextlib import asynccontextmanager
from fastapi import FastAPI,WebSocket
from fastapi.responses import FileResponse
from bot.api.routes import router
from bot.core.runtime import runtime
@asynccontextmanager
async def lifespan(app):
    await runtime.start(); yield; await runtime.stop()
def create_app():
    app=FastAPI(title='ISHClansOfClashBot',version='0.1.0',lifespan=lifespan); app.include_router(router,prefix='/api')
    @app.get('/',include_in_schema=False)
    async def index(): return FileResponse('web/index.html')
    @app.websocket('/ws/events')
    async def events(ws:WebSocket):
        await ws.accept(); await runtime.events.subscribe(ws)
        try:
            while True: await ws.receive_text()
        except Exception: await runtime.events.unsubscribe(ws)
    return app
app=create_app()
