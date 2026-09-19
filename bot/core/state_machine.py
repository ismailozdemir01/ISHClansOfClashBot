import asyncio,logging,time
from bot.core.models import BotState
log=logging.getLogger(__name__)
class StateMachine:
    def __init__(self,runtime): self.runtime=runtime; self.state=BotState.STOPPED; self.entered_at=time.monotonic()
    async def transition(self,state):
        if state!=self.state:
            log.info("state %s -> %s",self.state.value,state.value); self.state=state; self.entered_at=time.monotonic(); self.runtime.status.state=state
            await self.runtime.events.publish("state",{"state":state.value})
    def timed_out(self,timeout): return time.monotonic()-self.entered_at>timeout
    async def run(self):
        while self.runtime.status.running:
            try: await self.runtime.tick(self.state)
            except asyncio.CancelledError: raise
            except Exception as e:
                log.exception("state tick failed"); self.runtime.status.errors+=1; self.runtime.status.last_error=str(e); await self.transition(BotState.RECOVERY)
            await asyncio.sleep(self.runtime.settings.screenshot_interval)
