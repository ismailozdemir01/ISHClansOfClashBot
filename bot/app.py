from contextlib import asynccontextmanager
from fastapi import FastAPI,WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from bot.api.routes import router
from bot.core.runtime import runtime
@asynccontextmanager
async def lifespan(app): await runtime.start(); yield; await runtime.stop()
def create_app():
    app=FastAPI(title="ISHClansOfClashBot",version="0.1.0",lifespan=lifespan); app.include_router(router,prefix="/api"); app.mount("/static",StaticFiles(directory="web/static"),name="static")
    @app.get("/")
    async def index(): return FileResponse("web/index.html")
    @app.websocket("/ws/events")
    async def events(ws:WebSocket):
        await ws.accept(); await runtime.events.subscribe(ws)
        try:
            while True: await ws.receive_text()
        except Exception: await runtime.events.unsubscribe(ws)
    return app
