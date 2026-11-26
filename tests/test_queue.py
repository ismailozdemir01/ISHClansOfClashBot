from bot.army.composition import ArmyComposition, Unit
from bot.army.queue import ArmyQueue

def test_queue_consumes_without_losing_slot():
    queue=ArmyQueue(ArmyComposition([Unit("barbarian", 10, 2)]))
    assert queue.consume("barbarian", 3) == 7
    unit=queue.pending()[0]
    assert unit.count == 7
    assert unit.slot == 2

def test_queue_rejects_invalid_amount():
    queue=ArmyQueue(ArmyComposition([Unit("barbarian", 10, 2)]))
    try:
        queue.consume("barbarian", 0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
