from PIL import Image
import os
from pathlib import Path


filename = "../working/res/wildcat.png"
with Image.open(filename) as image:
    width, height = image.size
    print(image.size)


res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
print(res_path)


my_file = Path("../working/res/wildcat.png")
if my_file.is_file():
    print("True")