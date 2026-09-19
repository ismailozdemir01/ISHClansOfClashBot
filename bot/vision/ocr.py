import cv2
import pytesseract
from PIL import Image
class OcrReader:
    def __init__(self,enabled,language="eng"): self.enabled=enabled; self.language=language
    def read(self,image):
        if not self.enabled:return ""
        rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        return pytesseract.image_to_string(Image.fromarray(rgb),lang=self.language).strip()
