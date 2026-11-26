from bot.core.models import Target
from bot.strategy.config import StrategyConfig
from bot.strategy.target import TargetScorer

def test_target_score_and_accept():
    scorer=TargetScorer(StrategyConfig(min_score=0.1, min_gold=100000, min_elixir=100000))
    target=Target(gold=200000, elixir=200000, dark_elixir=1000, trophies=20, confidence=1.0)
    assert scorer.accept(target)
    assert target.score > 0.1

def test_target_rejects_low_loot():
    scorer=TargetScorer()
    assert not scorer.accept(Target(gold=1, elixir=1, confidence=1.0))

def test_town_hall_filter():
    scorer=TargetScorer(StrategyConfig(min_score=0.0, min_gold=1, min_elixir=1, max_town_hall=12))
    assert scorer.accept(Target(gold=100000, elixir=100000, town_hall=12, confidence=1.0))
    assert not scorer.accept(Target(gold=100000, elixir=100000, town_hall=13, confidence=1.0))
