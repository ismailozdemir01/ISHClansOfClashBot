import asyncio
from bot.core.config import get_settings
from bot.core.events import EventBus
from bot.core.logging import configure_logging
from bot.core.models import BotState,RuntimeStatus,Target
from bot.core.state_machine import StateMachine
from bot.adb.client import AdbClient
from bot.vision.pipeline import VisionPipeline
from bot.strategy.target import TargetScorer
from bot.attack.controller import AttackController
from bot.storage.repository import Repository

class Runtime:
    def __init__(self,settings=None):
        configure_logging()
        self.settings=settings or get_settings()
        self.events=EventBus()
        self.status=RuntimeStatus()
        self.adb=AdbClient(self.settings)
        self.vision=VisionPipeline(self.settings)
        self.scorer=TargetScorer()
        self.repo=Repository(self.settings.database_url)
        self.attack=AttackController(self)
        self.machine=StateMachine(self)
        self.task=None
        self.started=False

    async def emit(self,kind,payload):
        await self.events.publish(kind,payload)
        self.repo.log_event(kind,payload)

    async def start(self):
        if self.started: return
        self.repo.init()
        self.started=True
        await self.emit("system",{"message":"runtime ready"})

    async def stop(self):
        await self.stop_bot()
        self.started=False

    async def start_bot(self):
        if self.status.running: return
        self.status.running=True
        self.status.last_error=None
        self.task=asyncio.create_task(self.machine.run(),name="clash-bot-runtime")
        await self.emit("system",{"message":"bot started"})

    async def stop_bot(self):
        self.status.running=False
        if self.task:
            self.task.cancel()
            try: await self.task
            except asyncio.CancelledError: pass
            self.task=None
        self.status.state=BotState.STOPPED
        await self.emit("system",{"message":"bot stopped"})

    async def tick(self,state):
        if state==BotState.CONNECTING:
            self.status.connected=await self.adb.ensure_connected()
            await self.machine.transition(BotState.HOME if self.status.connected else BotState.RECOVERY)
        elif state==BotState.HOME:
            image=await self.adb.screenshot()
            detected=self.vision.detect_state(image)
            await self.machine.transition(BotState.ARMY if detected in {"home","army","unknown"} else BotState.RECOVERY)
        elif state==BotState.ARMY:
            await self.machine.transition(BotState.SEARCHING)
        elif state==BotState.SEARCHING:
            image=await self.adb.screenshot()
            if self.settings.dry_run and not self.settings.ocr_enabled:
                target=Target(gold=250000,elixir=220000,dark_elixir=1500,trophies=25,confidence=1.0)
            else:
                target=self.scorer.extract_target(image,self.vision)
            self.status.searches += 1
            await self.emit("search",{"target":target.__dict__})
            if self.scorer.accept(target):
                self.status.target=target
                await self.machine.transition(BotState.BATTLE)
            else:
                await self.attack.next_search()
        elif state==BotState.BATTLE:
            await self.attack.execute()
            self.status.attacks += 1
            await self.emit("attack",{"count":self.status.attacks})
            await self.machine.transition(BotState.RESULT)
        elif state==BotState.RESULT:
            self.status.target=None
            await asyncio.sleep(1)
            await self.machine.transition(BotState.HOME)
        elif state==BotState.RECOVERY:
            await self.attack.recover()
            await self.machine.transition(BotState.CONNECTING)
        elif state==BotState.UNKNOWN:
            await self.machine.transition(BotState.RECOVERY)
