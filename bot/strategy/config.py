from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class StrategyConfig:
    min_score: float=.55
    min_confidence: float=.5
    min_gold: int=100000
    min_elixir: int=100000
    min_dark: int=0
    max_town_hall: int|None=None
