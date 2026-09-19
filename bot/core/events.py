import asyncio
from datetime import datetime, timezone
from fastapi import WebSocket

class EventBus:
    def __init__(self): self._clients=set(); self._lock=asyncio.Lock()
    async def subscribe(self, ws:WebSocket):
        async with self._lock: self._clients.add(ws)
    async def unsubscribe(self, ws:WebSocket):
        async with self._lock: self._clients.discard(ws)
    async def publish(self, kind:str, payload:dict):
        event={"kind":kind,"timestamp":datetime.now(timezone.utc).isoformat(),"payload":payload}
        async with self._lock: clients=list(self._clients)
        for ws in clients:
            try: await ws.send_json(event)
            except Exception: await self.unsubscribe(ws)
