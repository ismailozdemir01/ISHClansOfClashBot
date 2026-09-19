from bot.actions.input import InputController
from bot.core.models import Point
class Fake:
    def __init__(self): self.calls=[]
    def tap(self,x,y): self.calls.append((x,y))
def test_dry_run():
    f=Fake(); InputController(f,dry_run=True,jitter=0).tap(Point(1,2)); assert f.calls==[]
