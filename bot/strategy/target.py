import re
from bot.core.models import Target
from bot.strategy.config import StrategyConfig

class TargetScorer:
    def __init__(self, config=None):
        self.config=config or StrategyConfig()

    def score(self, target: Target):
        loot=min(1.0, target.gold/300000 + target.elixir/300000 + target.dark_elixir/10000)
        trophy_bonus=min(0.15, max(0.0, target.trophies/500*0.15))
        return min(1.0, 0.7*loot + trophy_bonus)

    def accept(self, target: Target):
        target.score=self.score(target)
        if target.confidence < self.config.min_confidence:
            return False
        if target.gold < self.config.min_gold or target.elixir < self.config.min_elixir:
            return False
        if target.dark_elixir < self.config.min_dark or target.score < self.config.min_score:
            return False
        if self.config.max_town_hall is not None and target.town_hall is not None:
            if target.town_hall > self.config.max_town_hall:
                return False
        return True

    def extract_target(self, screen, vision):
        text=vision.text(screen)
        nums=[int(x.replace(",", "")) for x in re.findall(r"\d[\d,]*", text)]
        if len(nums) < 4:
            return Target(confidence=0.0)
        town_hall=nums[4] if len(nums) >= 5 and 1 <= nums[4] <= 18 else None
        return Target(
            gold=nums[0], elixir=nums[1], dark_elixir=nums[2],
            trophies=nums[3], town_hall=town_hall,
            confidence=min(1.0, 0.5 + min(len(nums), 5)*0.1)
        )
