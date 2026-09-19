import re
from bot.core.models import Target
class TargetScorer:
    def __init__(self,minimums=None): self.minimums=minimums or {"gold":100000,"elixir":100000,"dark_elixir":0,"trophies":0}
    def extract_target(self,screen,vision):
        text=vision.text(screen)
        if not text:return Target()
        nums=[int(x.replace(",","")) for x in re.findall(r"\\d[\\d,]*",text)]+[0]*4
        return Target(nums[0],nums[1],nums[2],nums[3],.5)
    def score(self,t): return t.gold+t.elixir+t.dark_elixir*10+t.trophies*100
    def accept(self,t):
        t.score=self.score(t)
        return t.confidence>0 and all(t.__dict__[k]>=v for k,v in self.minimums.items())
