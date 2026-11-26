import asyncio
import pytest
from bot.core.config import Settings
from bot.core.models import BotState
from bot.core.runtime import Runtime

@pytest.mark.asyncio
async def test_runtime_start_stop(tmp_path):
    settings=Settings(database_url=f"sqlite:///{tmp_path}/bot.db",dry_run=True,screenshot_interval=0.01)
    runtime=Runtime(settings)
    await runtime.start()
    await runtime.start_bot()
    await asyncio.sleep(0.03)
    assert runtime.status.running
    await runtime.stop_bot()
    assert runtime.status.state==BotState.STOPPED
