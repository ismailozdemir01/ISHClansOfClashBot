class VillageManager:
    def __init__(self,inputs): self.inputs=inputs
    async def collect(self): return {"collected":False,"reason":"requires calibrated profile"}
