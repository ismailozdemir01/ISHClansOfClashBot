import asyncio
import cv2
import numpy as np

class AdbError(RuntimeError): pass

class AdbClient:
    def __init__(self,settings): self.settings=settings; self.serial=settings.device_serial or None
    async def _run(self,*args,timeout=15):
        cmd=["adb"]+(["-s",self.serial] if self.serial else [])+list(args)
        p=await asyncio.create_subprocess_exec(*cmd,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
        out,err=await asyncio.wait_for(p.communicate(),timeout)
        if p.returncode: raise AdbError(err.decode(errors="replace").strip() or "adb command failed")
        return out
    async def devices(self):
        raw=await self._run("devices")
        return [x.split("\\t")[0] for x in raw.decode().splitlines() if "\\tdevice" in x]
    async def ensure_connected(self):
        if self.settings.dry_run: return True
        ds=await self.devices()
        if self.serial: return self.serial in ds
        if ds: self.serial=ds[0]; return True
        return False
    async def screenshot(self):
        if self.settings.dry_run: return np.zeros((self.settings.screen_height,self.settings.screen_width,3),np.uint8)
        data=await self._run("exec-out","screencap","-p")
        img=cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR)
        if img is None: raise AdbError("invalid screenshot")
        return img
    async def tap(self,x,y):
        if not self.settings.dry_run: await self._run("shell","input","tap",str(int(x)),str(int(y)))
    async def swipe(self,x1,y1,x2,y2,duration_ms=300):
        if not self.settings.dry_run: await self._run("shell","input","swipe",str(x1),str(y1),str(x2),str(y2),str(duration_ms))
    async def back(self):
        if not self.settings.dry_run: await self._run("shell","input","keyevent","4")
