import asyncio
from bot.actions.input import InputController

class Fake:
    def __init__(self):
        self.calls = []
    async def tap(self, x, y):
        self.calls.append((x, y))

def test_input_tap():
    fake = Fake()
    asyncio.run(InputController(fake, min_delay=0, max_delay=0).tap(1, 2))
    assert fake.calls == [(1, 2)]
