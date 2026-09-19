import re
from bot.core.models import Target
from bot.strategy.config import StrategyConfig

class TargetScorer:
    def __init__(self,config=None):
        self.config=config or StrategyConfig()

    def score(self,target:Target):
        loot=min(1.0,target.gold/300000+target.elixir/300000+target.dark_elixir/10000)
        trophy_bonus=min(0.15,max(0.0,target.trophies/500*0.15))
        return min(1.0,0.7*loot+trophy_bonus)

    def accept(self,target:Target):
        target.score=self.score(target)
        return (
            target.confidence >= 0.5 and
            target.gold >= self.config.min_gold and
            target.elixir >= self.config.min_elixir and
            target.dark_elixir >= self.config.min_dark and
            target.score >= self.config.min_score
        )

    def extract_target(self,screen,vision):
        text=vision.text(screen)
        nums=[int(x.replace(",","")) for x in re.findall(r"\d[\d,]*",text)][:4]
        nums += [0]*(4-len(nums))
        return Target(gold=nums[0],elixir=nums[1],dark_elixir=nums[2],trophies=nums[3],confidence=0.5 if nums else 0.0)
