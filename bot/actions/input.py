import asyncio,random
class InputController:
    def __init__(self,adb,min_delay=.12,max_delay=.35): self.adb=adb; self.min_delay=min_delay; self.max_delay=max_delay
    async def tap(self,x,y): await self.adb.tap(x,y); await asyncio.sleep(random.uniform(self.min_delay,self.max_delay))
    async def swipe(self,x1,y1,x2,y2,duration=300): await self.adb.swipe(x1,y1,x2,y2,duration); await asyncio.sleep(random.uniform(self.min_delay,self.max_delay))
