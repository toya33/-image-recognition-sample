import sys
import cv2
import pyocr
import numpy as np
from PIL import Image
image = "test.png"
name = "test"

def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

#original
img = cv2.imread(image)
#cv2.imwrite(f"1_{name}_original.png",img)

#gray
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imwrite(f"2_{name}_gray.png",img)

#threshold
th = 200
img = cv2.threshold(
    img
    , th
    , 255
    , cv2.THRESH_BINARY
)[1]
#cv2.imwrite(f"3_{name}_threshold_{th}.png",img)

#bitwise
img = cv2.bitwise_not(img)
#cv2.imwrite(f"4_{name}_bitwise.png",img)

#cv2.imwrite("target.png",img)

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
res = tool.image_to_string(
#   Image.open("target.png")
    cv2pil(img)
    ,lang="eng")

print(res)

'''reference
【Python】Pillow ↔ OpenCV 変換
    https://qiita.com/derodero24/items/f22c22b22451609908ee

pip で OpenCV のインストール
    https://qiita.com/fiftystorm36/items/1a285b5fbf99f8ac82eb

【Python】OpenCVとpyocrで画像から文字を認識してみる
    https://qiita.com/pon187/items/f9a70fd52cc91ddb4ed7
'''