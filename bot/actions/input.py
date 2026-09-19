import asyncio
import random

class InputController:
    def __init__(self, adb, min_delay=0.12, max_delay=0.35, jitter=0):
        self.adb = adb
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.jitter = jitter

    def _jittered(self, value):
        return int(value + random.uniform(-self.jitter, self.jitter)) if self.jitter else int(value)

    async def tap(self, x, y):
        await self.adb.tap(self._jittered(x), self._jittered(y))
        await asyncio.sleep(random.uniform(self.min_delay, self.max_delay))

    async def swipe(self, x1, y1, x2, y2, duration_ms=300):
        await self.adb.swipe(self._jittered(x1), self._jittered(y1), self._jittered(x2), self._jittered(y2), duration_ms)
        await asyncio.sleep(random.uniform(self.min_delay, self.max_delay))
