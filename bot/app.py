from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from bot.api.routes import bind
from bot.core.runtime import Runtime

BASE_DIR = Path(__file__).resolve().parent.parent

def create_app(runtime=None):
    runtime = runtime or Runtime()

    @asynccontextmanager
    async def lifespan(app):
        await runtime.start()
        yield
        await runtime.stop()

    app = FastAPI(title="ISHClansOfClashBot", version="0.1.0", lifespan=lifespan)
    app.include_router(bind(runtime), prefix="/api")

    @app.get("/", include_in_schema=False)
    async def index():
        return FileResponse(BASE_DIR / "web" / "index.html")

    return app

app = create_app()
