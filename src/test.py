#! .venv/Scripts/python.exe

#画面キャプチャ
import tkinter as tk
from PIL import Image,ImageGrab,ImageTk
#画像認識
import sys
import numpy as np
import cv2

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

img=None
pimg=None

def capture():
    global img,pimg
    #img=ImageGrab.grab(bbox=(0,0,200,160))
    #img=ImageGrab.grab(bbox=(0,0,3840,2160))
    img=ImageGrab.grab(bbox=(0,0,500,460))
    # Pillow → OpenCV
    new_cv_image = pil2cv(img)
    #2---グレイスケールに変換して二値化
    gray = cv2.cvtColor(new_cv_image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    #3---輪郭抽出
    contours = cv2.findContours(
    thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    #4---抽出した数分処理
    for moji in contours:
        x, y, w, h = cv2.boundingRect(moji)
        if h < 20: continue
        red = (0, 0, 255)
        cv2.rectangle(new_cv_image, (x, y), (x+w, y+h), red, 2)
    # OpenCV → Pillow
    new_pil_image = cv2pil(new_cv_image)
    # 画面表示
    pimg=ImageTk.PhotoImage(image=new_pil_image)
    canvas.create_image( 0,0, anchor="nw", image=pimg )

root=tk.Tk()
#root.state('zoomed')
button=tk.Button(root,text='Capture',command=capture)
button.pack()
canvas=tk.Canvas(root,bg='black')
canvas.pack()

root.mainloop()

#【Python応用】OpenCVを用いた文字認識を行ってみた
#https://www.hobby-happymylife.com/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0/python_opencv_ocr/

#pythonで画面キャプチャーツールを作ってみよう(2)
#https://www.mltlab.com/wp/archives/626

#【Python】Pillow ↔ OpenCV 変換
#https://qiita.com/derodero24/items/f22c22b22451609908ee