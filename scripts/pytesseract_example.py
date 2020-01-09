import re
import pytesseract
from PIL import Image

# https://github.com/tesseract-ocr/tesseract
pytesseract.pytesseract.tesseract_cmd = 'tesseract'
text = pytesseract.image_to_string(Image.open('18.png'))
# print(text)

target_re = re.compile(r"([0-9]{14})")
results = target_re.findall(text)
print(results)
