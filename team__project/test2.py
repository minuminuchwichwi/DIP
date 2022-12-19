from PIL import Image
from pytesseract import *

pytesseract.pytesseract.pytesseract.tesseract_cmd = r'C:/Users/이민우/AppData/Local/tesseract.exe'

image = Image.open("C:/text.png")

print1 = image_to_string(image, lang='kor', config='--psm 1 -c preserve_interword_spaces=1')

print(print1)

with open('text.txt', 'w', encoding='utf-8') as tx:
    tx.write(print1)