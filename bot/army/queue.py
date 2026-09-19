from dataclasses import dataclass
from bot.army.composition import ArmyComposition, Unit

@dataclass(slots=True)
class ArmyQueue:
    composition: ArmyComposition

    def pending(self):
        return [u for u in self.composition.units if u.count > 0]

    def consume(self, name: str, n: int=1):
        if n < 1:
            raise ValueError("n must be >= 1")
        for i, unit in enumerate(self.composition.units):
            if unit.name == name:
                remaining=max(0, unit.count-n)
                self.composition.units[i]=Unit(unit.name, remaining, unit.slot)
                return remaining
        raise KeyError(name)
