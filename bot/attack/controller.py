import asyncio
from bot.actions.input import InputController
from bot.attack.planner import AttackPlanner

class AttackController:
    def __init__(self, runtime):
        self.runtime = runtime
        self.inputs = InputController(runtime.adb)
        self.planner = AttackPlanner()

    async def next_search(self):
        await self.inputs.tap(self.runtime.settings.search_button_x, self.runtime.settings.search_button_y)

    async def execute(self):
        s = self.runtime.settings
        plan = self.planner.plan(s.screen_width, s.screen_height, unit="barbarian", count=10)
        for deployment in plan:
            for point in deployment.points:
                await self.inputs.tap(point.x, point.y)
        await asyncio.sleep(0.5)

    async def recover(self):
        await self.runtime.adb.back()
        await asyncio.sleep(0.5)
