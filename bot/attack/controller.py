import asyncio
from bot.actions.input import InputController
from bot.attack.planner import AttackPlanner
from bot.army.composition import ArmyComposition, Unit
from bot.army.manager import ArmyManager

class AttackController:
    def __init__(self, runtime):
        self.runtime=runtime
        self.inputs=InputController(runtime.adb)
        self.planner=AttackPlanner()
        self.army=ArmyManager(self.inputs)

    async def next_search(self):
        await self.inputs.tap(self.runtime.settings.search_button_x, self.runtime.settings.search_button_y)

    async def execute(self):
        s=self.runtime.settings
        composition=ArmyComposition([Unit(s.attack_unit_name, s.attack_unit_count, s.attack_unit_slot)])
        prepared=await self.army.prepare(composition)
        self.runtime.status.metadata["army"]=prepared
        await self.inputs.tap(s.attack_unit_x, s.attack_unit_y)
        plan=self.planner.plan(s.screen_width, s.screen_height, unit=s.attack_unit_name, count=s.attack_unit_count)
        for deployment in plan:
            for point in deployment.points:
                await self.inputs.tap(point.x, point.y)
        await asyncio.sleep(max(0.0, float(s.attack_settle_delay)))

    async def recover(self):
        await self.runtime.adb.back()
        await asyncio.sleep(max(0.0, float(self.runtime.settings.recovery_delay)))
