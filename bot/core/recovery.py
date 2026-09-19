import time, logging
class RecoveryManager:
    def __init__(self, adb, max_attempts=3): self.adb=adb; self.max_attempts=max_attempts; self.attempts=0; self.log=logging.getLogger('ishbot.recovery')
    def reset(self): self.attempts=0
    def recover(self):
        self.attempts+=1
        if self.attempts>self.max_attempts: return False
        try: self.adb.back()
        except Exception as e: self.log.warning('back failed: %s',e)
        time.sleep(.8); return True
