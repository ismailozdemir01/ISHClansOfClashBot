from dataclasses import replace
from bot.core.models import Target
from bot.strategy.config import StrategyConfig
class TargetScorer:
    def __init__(self, config=None): self.config=config or StrategyConfig()
    def score(self,t:Target):
        loot=min(1.0,t.gold/300000+t.elixir/300000+t.dark_elixir/10000)
        return min(1.0,.7*loot+.15*(t.trophies/500))
    def accept(self,t:Target):
        s=self.score(t); t.score=s
        return t.confidence>0 and t.gold>=self.config.min_gold and t.elixir>=self.config.min_elixir and t.dark_elixir>=self.config.min_dark and (self.config.max_town_hall is None or getattr(t,'town_hall',None) is None) and s>=self.config.min_score
    def extract_target(self,screen,vision):
        import re
        text=vision.text(screen)
        nums=[int(x.replace(',','')) for x in re.findall(r'\\d[\\d,]*',text)][:4]
        nums += [0]*(4-len(nums))
        return Target(gold=nums[0],elixir=nums[1],dark_elixir=nums[2],trophies=nums[3],confidence=.5)
