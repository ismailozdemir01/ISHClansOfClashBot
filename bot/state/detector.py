from bot.core.models import BotState

class StateDetector:
    def __init__(self, matcher=None, templates=None, threshold=0.78):
        self.matcher=matcher; self.templates=templates or {}; self.threshold=threshold
    def detect(self, image):
        if self.matcher is None: return BotState.UNKNOWN
        hits=[]
        import cv2
        for state,path in self.templates.items():
            t=cv2.imread(str(path))
            m=self.matcher.match(image,t,self.threshold) if t is not None else None
            if m: hits.append((m.score,state))
        return max(hits)[1] if hits else BotState.UNKNOWN
