from dataclasses import dataclass
from bot.core.models import Point
@dataclass(frozen=True,slots=True)
class Deployment:
    unit:str
    points:list[Point]
class AttackPlanner:
    def __init__(self,edge_margin=80): self.edge_margin=edge_margin
    def perimeter(self,w,h,count=12):
        pts=[]
        for i in range(count):
            x=int(self.edge_margin+(w-2*self.edge_margin)*i/max(1,count-1))
            pts.append(Point(x,self.edge_margin)); pts.append(Point(x,h-self.edge_margin))
        return pts[:count]
    def plan(self,w,h,unit='barbarian',count=12): return [Deployment(unit,self.perimeter(w,h,count))]
