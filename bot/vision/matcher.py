from pathlib import Path
import cv2
class Match:
    def __init__(self,name,score,x,y,width,height): self.name=name; self.score=float(score); self.x=x; self.y=y; self.width=width; self.height=height
    @property
    def center(self): return self.x+self.width//2,self.y+self.height//2
class TemplateMatcher:
    def __init__(self,template_dir): self.root=Path(template_dir)
    def match(self,image,name,threshold=.82):
        t=cv2.imread(str(self.root/name),cv2.IMREAD_COLOR)
        if t is None: return None
        r=cv2.matchTemplate(image,t,cv2.TM_CCOEFF_NORMED); _,score,_,loc=cv2.minMaxLoc(r)
        if score<threshold:return None
        h,w=t.shape[:2]; return Match(name,score,loc[0],loc[1],w,h)
