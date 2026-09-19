import asyncio
from bot.core.config import get_settings
from bot.core.events import EventBus
from bot.core.logging import configure_logging
from bot.core.models import BotState,RuntimeStatus
from bot.core.state_machine import StateMachine
from bot.adb.client import AdbClient
from bot.vision.pipeline import VisionPipeline
from bot.strategy.target import TargetScorer
from bot.attack.controller import AttackController
from bot.storage.repository import Repository

class Runtime:
    def __init__(self):
        configure_logging(); self.settings=get_settings(); self.events=EventBus(); self.status=RuntimeStatus(); self.adb=AdbClient(self.settings); self.vision=VisionPipeline(self.settings); self.scorer=TargetScorer(); self.attack=AttackController(self); self.repo=Repository(self.settings.database_url); self.machine=StateMachine(self); self.task=None
    async def start(self): self.repo.init(); await self.events.publish("system",{"message":"runtime ready"})
    async def stop(self): await self.stop_bot()
    async def start_bot(self):
        if self.status.running:return
        self.status.running=True; self.task=asyncio.create_task(self.machine.run()); await self.events.publish("system",{"message":"bot started"})
    async def stop_bot(self):
        self.status.running=False
        if self.task:
            self.task.cancel()
            try: await self.task
            except asyncio.CancelledError: pass
            self.task=None
        self.status.state=BotState.STOPPED; await self.events.publish("system",{"message":"bot stopped"})
    async def tick(self,state):
        if state==BotState.STOPPED: await self.machine.transition(BotState.CONNECTING)
        elif state==BotState.CONNECTING:
            self.status.connected=await self.adb.ensure_connected(); await self.machine.transition(BotState.HOME if self.status.connected else BotState.RECOVERY)
        elif state==BotState.HOME:
            await self.machine.transition(BotState.ARMY if self.vision.detect_state(await self.adb.screenshot()) in {"home","unknown"} else BotState.UNKNOWN)
        elif state==BotState.ARMY:
            await self.machine.transition(BotState.SEARCHING)
        elif state==BotState.SEARCHING:
            target=self.scorer.extract_target(await self.adb.screenshot(),self.vision); self.status.searches+=1
            if self.scorer.accept(target): self.status.target=target; await self.machine.transition(BotState.BATTLE)
            else: await self.attack.next_search()
        elif state==BotState.BATTLE:
            await self.attack.execute(); self.status.attacks+=1; await self.machine.transition(BotState.RESULT)
        elif state==BotState.RESULT:
            await asyncio.sleep(1); await self.machine.transition(BotState.HOME)
        else:
            await self.attack.recover(); await self.machine.transition(BotState.HOME)

runtime=Runtime()
