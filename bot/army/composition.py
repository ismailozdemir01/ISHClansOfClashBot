from dataclasses import dataclass
@dataclass(frozen=True)
class Unit: name:str; count:int; slot:int
@dataclass
class ArmyComposition:
    units:list[Unit]
    def total_units(self): return sum(u.count for u in self.units)
    @classmethod
    def from_dict(cls,data): return cls([Unit(str(x["name"]),int(x["count"]),int(x["slot"])) for x in data])
