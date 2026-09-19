from dataclasses import dataclass
from bot.army.composition import ArmyComposition,Unit
@dataclass(slots=True)
class ArmyQueue:
    composition: ArmyComposition
    def pending(self): return [u for u in self.composition.units if u.count>0]
    def consume(self,name,n=1):
        for i,u in enumerate(self.composition.units):
            if u.name==name:
                self.composition.units[i]=Unit(u.name,max(0,u.count-n)); return
        raise KeyError(name)
