from bot.vision.matcher import TemplateMatcher
from bot.vision.ocr import OcrReader
class VisionPipeline:
    def __init__(self,settings): self.matcher=TemplateMatcher(settings.template_dir); self.ocr=OcrReader(settings.ocr_enabled,settings.ocr_lang)
    def detect_state(self,image):
        for state,t in [("home","home.png"),("army","army.png"),("attack","attack.png"),("result","result.png")]:
            if self.matcher.match(image,t,.80): return state
        return "unknown"
    def text(self,image): return self.ocr.read(image)
