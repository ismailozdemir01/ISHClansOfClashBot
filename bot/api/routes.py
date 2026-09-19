from fastapi import APIRouter
from bot.core.runtime import runtime
router=APIRouter()
@router.get("/status")
async def status():
    s=runtime.status
    return {"state":s.state.value,"connected":s.connected,"running":s.running,"searches":s.searches,"attacks":s.attacks,"errors":s.errors,"last_error":s.last_error,"target":s.target.__dict__ if s.target else None}
@router.post("/start")
async def start(): await runtime.start_bot(); return {"ok":True}
@router.post("/stop")
async def stop(): await runtime.stop_bot(); return {"ok":True}
@router.get("/devices")
async def devices(): return {"devices":["dry-run"] if runtime.settings.dry_run else await runtime.adb.devices()}
@router.get("/health")
async def health(): return {"ok":True}
