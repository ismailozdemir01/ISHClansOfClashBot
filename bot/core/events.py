import asyncio
from collections import deque
from datetime import datetime, timezone
from fastapi import WebSocket

class EventBus:
    def __init__(self, max_history=200):
        self._clients=set()
        self._history=deque(maxlen=max_history)
        self._lock=asyncio.Lock()

    async def publish(self, kind:str, payload:dict):
        event={"kind":kind,"timestamp":datetime.now(timezone.utc).isoformat(),"payload":payload}
        async with self._lock:
            self._history.append(event)
            clients=list(self._clients)
        stale=[]
        for ws in clients:
            try:
                await ws.send_json(event)
            except Exception:
                stale.append(ws)
        if stale:
            async with self._lock:
                for ws in stale: self._clients.discard(ws)

    async def subscribe(self, ws:WebSocket):
        async with self._lock: self._clients.add(ws)

    async def unsubscribe(self, ws:WebSocket):
        async with self._lock: self._clients.discard(ws)

    async def recent(self, limit=50):
        async with self._lock:
            return list(self._history)[-max(1,min(limit,200)):]
