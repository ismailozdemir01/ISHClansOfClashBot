import asyncio
from bot.actions.input import InputController
class AttackController:
    def __init__(self,runtime): self.runtime=runtime; self.inputs=InputController(runtime.adb)
    async def next_search(self): await self.inputs.tap(0,0)
    async def execute(self): await asyncio.sleep(.5)
    async def recover(self): await self.runtime.adb.back(); await asyncio.sleep(.5)
