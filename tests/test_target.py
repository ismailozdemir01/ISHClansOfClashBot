from bot.core.models import Target
from bot.strategy.config import StrategyConfig
from bot.strategy.target import TargetScorer

def test_target_acceptance():
    scorer=TargetScorer(StrategyConfig(min_score=0.5,min_gold=100000,min_elixir=100000))
    target=Target(gold=250000,elixir=220000,dark_elixir=1500,trophies=25,confidence=1)
    assert scorer.accept(target)
    assert 0 <= target.score <= 1
