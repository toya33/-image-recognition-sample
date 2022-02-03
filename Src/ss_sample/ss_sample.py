import win32gui
import win32con
import pyautogui as pgui
import ctypes
import time
from PIL import ImageGrab

def foreground():
    #BlueStacksアプリのウィンドウを特定
    application = win32gui.FindWindow(None, "BlueStacks 2")
    #特定待ち時間
    time.sleep(1)
    #アプリのウィンドウを最前面へ移動
    win32gui.SetForegroundWindow(application)
    return application

def screenShot(application):
    rect = win32gui.GetWindowRect(application)
    ss = ImageGrab.grab(bbox=(rect[0], rect[1], rect[2], rect[3]))
    ss.show()

def main():
    app = foreground()
    screenShot(app)
    #print(find_window_name())

if __name__ == "__main__":
    main()


'''reference
pywin32によりPythonからWin32 APIにアクセスする
    https://self-development.info/pywin32%E3%81%AB%E3%82%88%E3%82%8Apython%E3%81%8B%E3%82%89win32-api%E3%81%AB%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E3%81%99%E3%82%8B/

Python win32gui.GetForegroundWindow() Examples
    https://www.programcreek.com/python/example/81370/win32gui.GetForegroundWindow

Python の win32gui を使ってアクティブウインドウの記録を取るスクリプトを作ってみた
    https://qiita.com/aikige/items/d7bdf26e2cb376268ed0

【Python】スクリーンショットを取得して指定フォルダに保存する（Pillow、selenium、PyAutoGUI）
    https://office54.net/python/app/python-screenshot-pillow
'''