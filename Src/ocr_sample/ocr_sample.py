import sys
import win32gui
import pyautogui as pgui
import ctypes
import time
from PIL import ImageGrab, Image
import cv2
import pyocr
import numpy as np

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


def foreground():
    #BlueStacksアプリのウィンドウを特定
    application = win32gui.FindWindow(None, "BlueStacks 2")
    #特定待ち時間
    time.sleep(1)
    #アプリのウィンドウを最前面へ移動
    win32gui.SetForegroundWindow(application)
    return application

def screenshot(application):
    rect = win32gui.GetWindowRect(application)
    ss = ImageGrab.grab(bbox=(rect[0], rect[1], rect[2], rect[3]))
    return ss

def image_processing(image):
    #openCV型の画像に変換
    img = pil2cv(image)
    #グレースケールへ変換
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #二値化
    th = 200
    img = cv2.threshold(
        img
        , th
        , 255
        , cv2.THRESH_BINARY
    )[1]
    #bitwise
    img = cv2.bitwise_not(img)
    #PIL型の画像に変換
    return cv2pil(img)

def ocr(image):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]
    res = tool.image_to_string(
        image,
        lang="jpn",
        builder=pyocr.builders.LineBoxBuilder(tesseract_layout=6)
    )
    return res

def ocr2(image):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]
    res = tool.image_to_string(
        image,
        lang="eng",
        builder=pyocr.builders.LineBoxBuilder(tesseract_layout=6)
    )
    return res

def app_click(application):
    ss = screenshot(application)
    img = image_processing(ss)
    line_boxs = ocr(img)
    rect = win32gui.GetWindowRect(application)
    for line_box in line_boxs:
        for word_box in line_box.word_boxes:
            if word_box.content == "陸":              
                pgui.click(
                    x=rect[0]+word_box.position[0][0],
                    y=rect[1]+word_box.position[0][1]
                )

def app_click2(application):
    ss = screenshot(application)
    img = image_processing(ss)
    img.show()
    line_boxs = ocr2(img)
    '''
    if len(line_boxs) > 0:
        rect = win32gui.GetWindowRect(application)
        for num in range(20,0,-1):
            for line_box in line_boxs:
                for word_box in line_box.word_boxes:
                    if word_box.content == num:              
                        pgui.click(
                            x=rect[0]+word_box.position[0][0],
                            y=rect[1]+word_box.position[0][1]
                        )
                break
    '''
    for line_box in line_boxs:
        print(line_box.content)



def main():
    #アプリケーションを最前面に表示
    app = foreground()
    #クリック
    #app_click(app)

    app_click2(app)

if __name__ == "__main__":
    main()