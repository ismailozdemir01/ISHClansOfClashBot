from collections import deque
from datetime import datetime, timezone

class EventBus:
    def __init__(self, max_history=200):
        self._history = deque(maxlen=max_history)

    def publish(self, kind: str, payload: dict):
        event = {"kind": kind, "timestamp": datetime.now(timezone.utc).isoformat(), "payload": payload}
        self._history.append(event)
        return event

    def recent(self, limit=50):
        limit = max(1, min(int(limit), len(self._history) or 1))
        return list(self._history)[-limit:]
