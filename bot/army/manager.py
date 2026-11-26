from bot.army.composition import ArmyComposition
class ArmyManager:
    def __init__(self,inputs): self.inputs=inputs
    async def prepare(self,composition:ArmyComposition): return {"ready":True,"units":composition.total_units()}
